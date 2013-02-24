#!/usr/bin/python

import os
import sys
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
			
def get_server_name(argv):
	### Get the server name: if there is a "@" the server is the second member 
	### if not the server is the entire arg
	
	if re.search(r"@", argv):
		return re.sub(r".*@(.*)",r"\1",argv)
	else:
		return argv
			
def process(server):
	### This function configures and execute our new ssh session
	### Mini plan:
	###		- Get the server name for log and window title
	###		- Write the log
	###		- Execute the command
		
	# Write the log for connection
	my_pid = str(os.getpid())
	write_log(my_pid, server, True)
		
	# Arguments for the execv command
	args = ["xterm", "-title", "server: " + server + " pid: " + my_pid]
	# Execute the command, here we have an only program and an only path. Change will be make...
	os.execv("/usr/bin/xterm", args)
	
def father(child_pid, server):
	### This function waits for the child process and finishes the log
	### Mini plan:
	###		- Wait method
	###		- Write the log
	
	# Wait for the child ending to avoid zombies
	os.wait()
	
	# Write the log when disconnect
	pid_str = str(child_pid)
	write_log(pid_str, server, False)
	
def main():
	#Work in porgress: Make test on the argv
	
	# Fork a new process for our session
	pid = os.fork()
	
	# Get the server name
	server = get_server_name(sys.argv[1])
	
	# Switch/case for fork result
	if pid == -1:
		# Work in progress: get exception
		print("Error")
	elif pid == 0:
		# We are with the child so we execute our process
		process(server)
		os._exit(0)
	else:
		# We are with the parent so we execute the parent process
		# parent(), work in progress
		father(pid, server)


main()
