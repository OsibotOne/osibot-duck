import shutil
import os
import zipfile
from datetime import datetime

# Get date now
now = datetime.now().strftime("%Y-%m-%d")
try:
    # Folder location
    backup_folder = "backup/"
    original_folders = ["data/", "logs/", "images/"]

    # |------------------------------Internal Backup---------------------------------------|
    for folder in original_folders:
        shutil.copytree(folder, os.path.join(backup_folder, folder),
                        dirs_exist_ok=True)  # Keep the original folder after coping
        
        # Delete all original files that have been copied
        for dir_path, dir_names, filenames in os.walk(folder):
            for file in filenames:
                os.remove(os.path.join(dir_path, file))

        # compress each folder as a separate file in the folder "backups" and add date to the end of each file.
        with zipfile.ZipFile(f"{backup_folder}{folder[:-1]}_backup_{now}.zip", "w") as zipf:
            for file in os.listdir(f"{backup_folder}{folder}"):
                zipf.write(os.path.join(backup_folder, folder, file))
    # |--------------------------End of Internal Backup------------------------------------|


    # |----------------------------Copy Backup to SSD--------------------------------------|
    # Check external SSD is accessible, if yes,
    ssd_path = "./ssd"
    if os.path.exists(ssd_path):
        # copy compressed files to external SSD storage
        compress_files = [file for file in os.listdir(backup_folder) if file.endswith(".zip")]
        for file in compress_files:
            shutil.copy(f"{backup_folder}{file}", ssd_path)
        # delete all files
        for file in compress_files:
            os.remove(f"{backup_folder}{file}")
    else:
        print("SSD is not accessible")

    # confirm all files have been copied to external SSD storage
    copied_files = os.listdir(ssd_path)
    is_copied = True
    for file_name in copied_files:
        if now not in file_name:
            is_copied = False
    if is_copied:
        print("Files has been copied")

    # Add backup report to log file.
    report = f"Backup completed on {now}."
    with open("backup_log.dat", "a") as log_file:
        log_file.write(now + "Back up completed \n")
    # |---------------------------End of copy to SSD---------------------------------------|

# If error occur
except Exception as error:
    report = f"{now} {type(error).__name__}: {error})"
    print(report)
    with open("./backup/backup_log.dat", "a") as log_file:
        log_file.write(report + "\n")
