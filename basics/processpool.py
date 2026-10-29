
import logging
from concurrent.futures import ProcessPoolExecutor

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(processName)s | %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)


def calculate_square(number: int):
    logger.debug("Starting calculation for number=%s", number)
    result = number * number
    logger.info("Calculation completed for number=%s, result=%s", number, result)
    return result


if __name__ == "__main__":
    pool = ProcessPoolExecutor(max_workers=5)
    try:
        futures = [pool.submit(calculate_square, n) for n in range(1, 6)]
        for future in futures:
            logger.info("Result: %s", future.result())
    except Exception:
        logger.exception("Executor task failed")
    finally:
        pool.shutdown()
        logger.info("Executor shut down")

    try:
        with ProcessPoolExecutor(max_workers=5) as pool:
            futures = [pool.submit(calculate_square, n)for n in range(6, 11)]
            for future in futures:
                logger.info("Result: %s", future.result())
    except Exception:
        logger.exception("Executor task failed")

    logger.info("Program finished")
