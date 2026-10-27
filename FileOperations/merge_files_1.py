from pathlib import Path

def merge_two_files(file1_path, file2_path, output_path):
    # Do not allow the output to overwrite an input.
    output = Path(output_path).resolve()
    inputs = {
        Path(file1_path).resolve(),
        Path(file2_path).resolve(),
    }

    if output in inputs:
        raise ValueError("Output path must differ from input paths")

    def next_name(file):
        line = file.readline()
        if line == "":
            return None
        return line.rstrip("\r\n")

    with (
        open(file1_path, "r", encoding="utf-8") as f1,
        open(file2_path, "r", encoding="utf-8") as f2,
        open(output_path, "w", encoding="utf-8") as out,
    ):
        name1 = next_name(f1)
        name2 = next_name(f2)

        while name1 is not None and name2 is not None:
            if name1 <= name2:
                out.write(name1 + "\n")
                name1 = next_name(f1)
            else:
                out.write(name2 + "\n")
                name2 = next_name(f2)

        while name1 is not None:
            out.write(name1 + "\n")
            name1 = next_name(f1)

        while name2 is not None:
            out.write(name2 + "\n")
            name2 = next_name(f2)


merge_two_files("file1.txt", "file2.txt", "merged.txt")
# BASE = Path(__file__).resolve().parent
# merge_two_files(BASE / "file1.txt", BASE / "file2.txt", BASE / "merged.txt")