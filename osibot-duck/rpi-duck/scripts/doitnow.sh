# osibot-duck

# Main Remote Command Script


# Does doit.now file exist? If No, exit script.


# Read /home/pi/command/doit.now file
# {CommandNumber},{CommandName},{CommandVariable1},{CommandVariable2},{CommandVariable3};
# 1,upload-backup.py;
# 2,goto-now.py,14.783687328434,-129.2323232737237;
# 3,relay-manual.py,6,1,0;



# Execute commands (run scripts in order sequence)



# Write all log outputs to /home/pi/now/result.now  (Overwrite file if already present)
# Also write log outputs like normal by amending to /home/pi/data/vessel.dat
# doitnow.py:{Date&Time}:{Output}
# doitnow.py:{Date&Time}:{New Commands Received}     If file exists
# doitnow.py:{Date&Time}:{New Commands Executed Successfuly}
# doitnow.py:{Date&Time}:{New Commands Executed Unsuccessfuly - {error msg}}


# delete doit.now file even if error occurs.




