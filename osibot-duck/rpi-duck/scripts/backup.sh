# osibot-duck

# Daily Backup Script


# copy /home/pi/data/vessel.dat to /home/pi/backup/data/vessel{DATE&TIME}.dat
# copy /home/pi/data/vessel.dat to /home/pi/backup/now/vessel.dat
# clear all data in vessel.dat

# copy /home/pi/data/science.dat to /home/pi/backup/data/science{DATE&TIME}.dat
# copy /home/pi/data/science.dat to /home/pi/backup/now/science.dat
# clear all data in science.dat

# copy /home/pi/log/vessel.log to /home/pi/backup/data/vessel{DATE&TIME}.log
# clear all data in vessel.log

# copy /home/pi/log/comms.log to /home/pi/backup/data/comms{DATE&TIME}.log
# clear all data in comms.log

# compress all 4 new files in folder backup/data into backup/old/data/data-backup-{DATE&TIME}.zip
# output to vessel.log file     backup.py:{Date&Time}:{Data Backup Complete}

# copy all files in /home/pi/pics/cam1/ to /home/pi/backup/pics/cam1/
# remove all files in /home/pi/pics/cam1/
# remove file /home/pi/backup/now/cam1-backup.zip
# compress all files in /home/pi/backup/pics/cam1/ to /home/pi/backup/now/cam1-backup.zip 
# copy cam2-backup.zip to /home/pi/backup/old/cam1/cam1-backup-{DATE&TIME}.zip
# remove all files in /home/pi/backup/pics/cam1/
# output to vessel.log file     backup.py:{Date&Time}:{Cam1 Backup Complete}

# copy all files in /home/pi/pics/cam2/ to /home/pi/backup/pics/cam2/
# remove all files in /home/pi/pics/cam2/
# remove file /home/pi/backup/now/cam2-backup.zip
# compress all files in /home/pi/backup/pics/cam2/ to /home/pi/backup/now/cam2-backup.zip 
# copy cam2-backup.zip to /home/pi/backup/old/cam2/cam2-backup-{DATE&TIME}.zip
# remove all files in /home/pi/backup/pics/cam2/
# output to vessel.log file     backup.py:{Date&Time}:{Cam2 Backup Complete}


# copy all 3 newly created .zip files to {External Drive Location}
# output to vessel.log file     backup.py:{Date&Time}:{BlackBox Updated}

# output to vessel.log file     backup.py:{Date&Time}:{Daily Backup Completed Successfully}
#or
# output to vessel.log file     backup.py:{Date&Time}:{Daily Backup Completed Unsuccessfully - {Error msg}}


