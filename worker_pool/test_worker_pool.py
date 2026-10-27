
import threading
import time
import unittest
from unittest.mock import patch

from worker_pool import run, TemporaryError


class TestWorkerPool(unittest.TestCase):

    def test_empty_input(self):
        """An empty input list should produce no jobs."""
        results, metrics = run([])

        self.assertEqual(results, [])
        self.assertEqual(metrics["submitted"], 0)
        self.assertEqual(metrics["succeeded"], 0)

    def test_successful_jobs(self):
        """Successful jobs should return their expected results."""
        results, metrics = run(
            [2, 3, 4],
            worker_count=2,
            max_pending=2,
        )

        self.assertEqual(
            [item["result"] for item in results],
            [4, 9, 16],
        )
        self.assertTrue(all(item["error"] is None for item in results))
        self.assertEqual(metrics["succeeded"], 3)
        self.assertEqual(metrics["failed"], 0)

    def test_results_preserve_input_order(self):
        """Results should follow input order, not completion order."""

        def controlled_process(value, job_cancel, deadline, attempt):
            # Make the first input finish last.
            time.sleep({1: 0.08, 2: 0.01, 3: 0.03}[value])
            return value * 10

        with patch("worker_pool.process", side_effect=controlled_process):
            results, _ = run(
                [1, 2, 3],
                worker_count=3,
                max_pending=3,
            )

        self.assertEqual(
            [item["result"] for item in results],
            [10, 20, 30],
        )

    def test_permanent_failure_is_recorded(self):
        """Invalid input should fail without retrying."""
        results, metrics = run(
            [-2],
            worker_count=1,
            max_pending=1,
        )

        self.assertIsNone(results[0]["result"])
        self.assertIn("Negative input", results[0]["error"])
        self.assertEqual(metrics["failed"], 1)
        self.assertEqual(metrics["retries"], 0)
        self.assertEqual(metrics["attempts"], 1)

    def test_transient_failure_is_retried(self):
        """A transient error should retry and eventually succeed."""
        results, metrics = run(
            [7],
            worker_count=1,
            max_pending=1,
            job_timeout=5.0,
        )

        self.assertEqual(results[0]["result"], 49)
        self.assertEqual(results[0]["attempts"], 3)
        self.assertEqual(metrics["retries"], 2)
        self.assertEqual(metrics["attempts"], 3)
        self.assertEqual(metrics["succeeded"], 1)

    def test_retry_limit(self):
        """After the retry limit, the job should fail."""

        def always_fail(value, job_cancel, deadline, attempt):
            raise TemporaryError("Temporary failure")

        with patch("worker_pool.process", side_effect=always_fail):
            results, metrics = run(
                [10],
                worker_count=1,
                max_pending=1,
                job_timeout=5.0,
            )

        self.assertIn("Temporary failure", results[0]["error"])
        self.assertEqual(metrics["attempts"], 4)
        self.assertEqual(metrics["retries"], 3)
        self.assertEqual(metrics["failed"], 1)

    def test_job_timeout(self):
        """A cooperative worker should stop when its deadline expires."""

        def slow_cooperative_process(
            value,
            job_cancel,
            deadline,
            attempt,
        ):
            # Simulate long work that responds to cancellation.
            job_cancel.wait(1.0)

            if job_cancel.is_set():
                raise RuntimeError("Job cancelled")

            return value * value

        with patch(
            "worker_pool.process",
            side_effect=slow_cooperative_process,
        ):
            results, metrics = run(
                [5],
                worker_count=1,
                max_pending=1,
                job_timeout=0.1,
            )

        self.assertIn("timed out", results[0]["error"].lower())
        self.assertEqual(metrics["timed_out"], 1)

    def test_bounded_concurrency(self):
        """Running jobs should never exceed worker_count."""
        lock = threading.Lock()
        active = 0
        max_active = 0

        def tracked_process(value, job_cancel, deadline, attempt):
            nonlocal active, max_active

            with lock:
                active += 1
                max_active = max(max_active, active)

            try:
                time.sleep(0.03)
                return value * value
            finally:
                with lock:
                    active -= 1

        with patch("worker_pool.process", side_effect=tracked_process):
            results, _ = run(
                list(range(10)),
                worker_count=2,
                max_pending=2,
            )

        self.assertEqual(len(results), 10)
        self.assertLessEqual(max_active, 2)
        self.assertTrue(all(item["error"] is None for item in results))

    def test_metrics_are_consistent(self):
        """Basic counters should agree with completed outcomes."""
        results, metrics = run(
            [1, -1, 2],
            worker_count=2,
            max_pending=2,
        )

        successful = sum(item["error"] is None for item in results)
        failed = sum(item["error"] is not None for item in results)

        self.assertEqual(metrics["submitted"], len(results))
        self.assertEqual(metrics["succeeded"], successful)
        self.assertEqual(metrics["failed"], failed)
        self.assertEqual(
            metrics["succeeded"] + metrics["failed"],
            len(results),
        )
        self.assertGreaterEqual(metrics["average_duration_seconds"], 0)


if __name__ == "__main__":
    unittest.main()
