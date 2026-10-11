import heapq

def merge_k_files(input_files, output_file):
    heap = []
    # Open every file
    files = [open(file, "r") for file in input_files]

    # Read first line from each file
    for index, file in enumerate(files):
        line = file.readline()

        if line:
            heapq.heappush(
                heap,
                (line.rstrip("\n"), index)
            )

    with open(output_file, "w") as out:

        while heap:

            smallest_name, file_index = heapq.heappop(heap)

            out.write(smallest_name + "\n")

            next_line = files[file_index].readline()

            if next_line:
                heapq.heappush(
                    heap,
                    (next_line.rstrip("\n"), file_index)
                )

    for file in files:
        file.close()
        