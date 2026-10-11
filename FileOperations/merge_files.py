import os

def merge_files(file1_path, file2_path, output_path):
    with open(file1_path, "r") as f1, \
         open(file2_path, "r") as f2, \
         open(output_path, "w") as out:

        line1 = f1.readline()
        line2 = f2.readline()
        print("reading files")
        while line1 and line2:
            # Remove only the newline for comparison and writing
            name1 = line1.rstrip("\n")
            name2 = line2.rstrip("\n")

            if name1 <= name2:
                out.write(name1 + "\n")
                line1 = f1.readline()
            else:
                out.write(name2 + "\n")
                line2 = f2.readline()

        # Write remaining lines from file1
        while line1:
            out.write(line1.rstrip("\n") + "\n")
            line1 = f1.readline()

        # Write remaining lines from file2
        while line2:
            out.write(line2.rstrip("\n") + "\n")
            line2 = f2.readline()


script_dir = os.path.dirname(os.path.abspath(__file__))

file1 = os.path.join(script_dir, "file1.txt")
file2 = os.path.join(script_dir, "file2.txt")
output = os.path.join(script_dir, "merged.txt")

merge_files(file1, file2, output)
