import shutil
import os
import zipfile
from datetime import datetime


def backup_internal(backup_folder, original_folders, date):
    """Backup "data", "log", "image" folders to internal "backup" folder
       Compress each folder individually as zip files

       Args:
           backup_folder (str): backup folder location
           original_folders (list): list of folders to back up
           date (str): date

       Returns:
           backup results
    """
    try:
        # scan for each folder
        for folder in original_folders:
            shutil.copytree(folder, os.path.join(backup_folder, folder),
                            dirs_exist_ok=True)  # Keep the original folder after coping
            # delete all original files that have been copied
            for dir_path, dir_names, filenames in os.walk(folder):
                for file in filenames:
                    os.remove(os.path.join(dir_path, file))

            # compress each folder as a separate file in the folder "backups" and add date to the end of each file.
            with zipfile.ZipFile(f"{backup_folder}{folder[:-1]}_backup_{date}.zip", "w") as zipf:
                for file in os.listdir(f"{backup_folder}{folder}"):
                    zipf.write(os.path.join(backup_folder, folder, file),
                               arcname=os.path.join(folder, file))
    except Exception as e:
        return f"error: Internal backup error:{e}"
    else:
        return "Internal backup done"


def backup_external(backup_folder, external_folder, date):
    """Copy zip files to SSD

        Args:
            backup_folder (str): internal backup location
            external_folder (str): external path
            date (str): date
        Returns:
            copy results
    """
    # Check external SSD is accessible
    try:
        if os.path.exists(external_folder):
            # Get list of all "zip" filenames
            compress_files = [file
                              for file in os.listdir(backup_folder)
                              if file.endswith(".zip")]
            # Copy compressed files to external SSD storage
            for file in compress_files:
                shutil.copy(f"{backup_folder}{file}", external_folder)

        else:
            return "SSD is not accessible"

    except Exception as e:
        return f"error: External backup error:{e}"

    else:
        # confirm all files have been copied to external SSD storage
        copied_files = os.listdir(external_folder)
        is_copied = True
        copy_failed = ""  # empty store failed copy files
        for file_name in copied_files:
            if date not in file_name:
                copy_failed = copy_failed + "," + file_name
                is_copied = False
        if is_copied:
            for file in compress_files:
                # Delete file after copied
                os.remove(f"{backup_folder}{file}")
            return "Files has copied to SSD"

        else:
            return f"Copied is incomplete: {copy_failed}"


def main():
    # Get date now
    now = datetime.now().strftime("%Y-%m-%d")
    # Folder location
    backup_folder = "backup/"
    original_folders = ["data/", "logs/", "images/"]
    ssd_path = "./ssd"
    # Run backup and get report
    report_bk_internal = backup_internal(backup_folder, original_folders, now)
    report_bk_ssd = backup_external(backup_folder, ssd_path, now)
    # Add backup report to log file.
    report_final = f"{report_bk_internal}\n{report_bk_ssd}:{now}\n"
    with open("./backup/backup_log.dat", "a") as log_file:
        log_file.write(report_final)


# The script can run individually or be part of other program.
if __name__ == "__main__":
    main()
