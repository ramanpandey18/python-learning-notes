
import heapq
from contextlib import ExitStack
from pathlib import Path


def merge_k_files(input_files, output_file):
    if not input_files:
        raise ValueError("At least one input file is required")

    output_path = Path(output_file).resolve()
    input_paths = [Path(path).resolve() for path in input_files]

    if output_path in input_paths:
        raise ValueError("Output file must differ from input files")

    heap = []

    with ExitStack() as stack:
        # Open every input file and register it for automatic closing.
        files = [
            stack.enter_context(
                open(path, "r", encoding="utf-8", newline="")
            )
            for path in input_paths
        ]

        def read_name(file):
            line = file.readline()

            if line == "":
                return None

            return line.rstrip("\r\n")

        # Add the first name from each non-empty file.
        for index, file in enumerate(files):
            name = read_name(file)

            if name is not None:
                heapq.heappush(heap, (name, index))

        # The output is opened only after the inputs are opened.
        with open(
            output_path, "w", encoding="utf-8", newline="\n"
        ) as out:

            while heap:
                smallest_name, file_index = heapq.heappop(heap)

                out.write(smallest_name + "\n")

                # Advance only the file that supplied this name.
                next_name = read_name(files[file_index])

                if next_name is not None:
                    heapq.heappush(
                        heap, (next_name, file_index)
                    )


if __name__ == "__main__":
    merge_k_files(
        ["file1.txt", "file2.txt", "file3.txt"],
        "merged.txt",
    )
