#!/usr/bin/python2

import os
import sys
import re

def child():
	print('A new child ' + str(os.getpid()) + '\n')
	os._exit(0)
	
def parent():
	newpid = os.fork()
	if newpid == 0:
		child()
	else:
		pids = (os.getpid(), newpid)
		print('parent: %d, child: %d' %pids)
			
			
def process(argv):
	### This function configures and execute our new ssh session
	### Mini plan:
	###		- Get the server name for log and window title
	###		- Write the log
	###		- Execute the command
	
	
	# Get the server name: if there is a "@" the server is the second member 
	#+if not the server is the entire arg
	if re.search(r"@", argv):
		server = re.sub(r".*@(.*)",r"\1",argv)
	else:
		server = argv
		
	#Work in progress: write the log
		
	# Arguments for the execv command
	args = ["xterm", "-title", "server: " + server + " pid: " + str(os.getpid())]
	# Execute the command, here we have an only program and an only path. Change will be make...
	os.execv("/usr/bin/xterm", args)
	
def father():
	### This function waits for the child process and finishes the log
	### Mini plan:
	###		- Wait method
	###		- Write the log
	
	# Wait for the child ending to avoid zombies
	os.wait()
	
	# Work in progress: write the log when disconnect
	print("Child killed")
	
def main():
	#Work in porgress: Make test on the argv
	
	# Fork a new process for our session
	pid = os.fork()
	
	# Switch/case for fork result
	if pid == -1:
		# Work in progress: get exception
	elif pid == 0:
		# We are with the child so we execute our process
		process(sys.argv[1])
		os._exit(0)
	else:
		# We are with the parent so we execute the parent process
		# parent(), work in progress
		father()


main()
