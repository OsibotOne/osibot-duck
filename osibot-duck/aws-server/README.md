# osibot-duck

This folder is for code that will be deployed on the AWS control server  for command and control and web dashboard.


1. Web Dashboard
	a) Display Latest Data
	b) Display track on map
	c) Display latest uploaded image

*Is there an open source solution to create this web dashboard? or just use nginx?


2. SFTP Server for vessel to upload data and images to and download new commands.

/upload/log/			*daily log files
/upload/data/			*daily data dumps
/upload/now/			*30 minute website update - location, data, cam1 pic, cam2 pic

/download/doit.now		*This file contains any new commands for vessel - manual upload.

*This is a very simple setup, see below.
https://tecadmin.net/setup-sftp-server-on-ubuntu/

