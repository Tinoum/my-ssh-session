#!/usr/bin/python2

import re
import shutil
import time

def write_log(pid_ssh, server, connect):
	
	### Write a log file with timestamp, server and pid when start and close ssh session
	### Log file is in this format:
	###			### Server: www.foo.bar with PID:1234234 
	###			Connection: 22 February 2013 10:40
	###			Disconnection: 22 February 2013 10:42
	
	# Chose here your file name	
	log_file = './coucou'
	
	# log_tmp: temp file in which we write the new log file (needed for disconnection)
	log_tmp = log_file + '.tmp'
	# log_old: saved logfile to avoid losing data
	log_old = log_file + '.old'

	# timestmp: time formated for human reading in log file
	timestmp = time.strftime("%d %B %Y %H:%M")
	# found_pid: boolean needed to write disconnection sentance after the connection one
	found_pid = False
	
	# If disconnection:
	if connect == False:
		with open(log_tmp,'w') as dest:
			with open(log_file,'r') as source:
					for line in source:
						# Copy the log line in the temp file
						dest.write(line)
						
						# If we did not find our PID yet
						if found_pid == False:
							# If we find the PID found_pid becomes True, else we do nothing to go to the next line
							if re.search(re.compile(r"^###.*%s.*$"%pid_ssh), line):
								found_pid = True
						
						# The PID was found so we can write the diconnection sentance
						else:
							dest.write('Disconnection: ' + timestmp + '\n')
							found_pid = False
							
		# Save the log file and rename the temp one
		shutil.copy(log_file,log_old)
		shutil.move(log_tmp,log_file)
		
	# If connection, just appends the header and the connection sentance to the log file
	else:
		with open(log_file, 'a') as my_file:
			my_file.write('\n### Server:' + server + ' with PID:' + pid_ssh + ' \n')
			my_file.write('Connection: ' + timestmp + '\n')

#write_log('1234234', 'google', True)
write_log('1234234', 'google', False)
