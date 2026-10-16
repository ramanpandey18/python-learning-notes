import glob
import shutil
import os
import zipfile

os.makedirs("archive", exist_ok=True)

for file_path in glob.glob("logs/*.log"):
    shutil.move(file_path, "archive/")

print("All log files moved.")

with zipfile.ZipFile("backup.zip", "w",
                     compression=zipfile.ZIP_DEFLATED) as zip_file:
    zip_file.write("main.py")
    zip_file.write("notes.txt")

with zipfile.ZipFile("backup.zip", "r") as zip_file:
    zip_file.extractall("extracted")

import zipfile

with zipfile.ZipFile("backup.zip", "r") as zip_file:
    for name in zip_file.namelist():
        print(name)

with zipfile.ZipFile("backup.zip", "r") as zip_file:
    with zip_file.open("notes.txt") as file:
        content = file.read().decode("utf-8")
        print(content)

log_files = glob.glob("logs/*.log")

if not log_files:
    print("No log files found.")
else:
    # Step 1: Create a ZIP archive
    with zipfile.ZipFile(
        "logs.zip",
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:
        for file_path in log_files:
            zip_file.write(file_path)

    # Step 2: Move the original files
    os.makedirs("archive", exist_ok=True)

    for file_path in log_files:
        shutil.move(file_path, "archive/")

    print("Logs compressed and archived.")

# Use shutil.make_archive() when you want to archive a whole directory with minimal code. 
# Use zipfile when you need fine-grained control over individual files, archive contents, 
# compression, or reading ZIP entries.