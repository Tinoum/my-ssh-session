Created by Quentin MARY


my-ssh-session
==============

### Descritpion:
Open new ssh session with log for timestamp, server and pid. For now the ssh session is open in a new XTerm window.

### Installation instructions
In the master branch, the programm is written in C, you just have to compile it with gcc.
In the code_in_python, the code is written in... Python ! I have condensed the source code in only one file. Execute it as other Python scripts.

I use it with an alias in Linux such as 'zx'. So I just type "zx foo@bar" to ssh to the bar server (and keep some trace of it)

### Where to get help
As it is a personnal (very small) project, I do not have a wiki or a web page. Otherwise you can email me at quentin.mmary@gmail.com

### Contribution guidelines
This project is a training to system and python programmation. I do not want to be help in code but you can send new ideas to improve the features.

### Contributor list
Me, myself and I, Quentin MARY, 22 years old, FRANCE.

### Inspiration
The basic idea is not so complicated so I think there are many other project like mine. I do not want to plagiarize them, just create it by my own.

### ToDo list
  - Chose between C and Python language ^^
  - Raise exceptions to secure a little more
  - Make and parse conf file (with configparser)
  - Enable options (as -t for a XTerm window - without ssh)
  - Remove Xterm, urxvt...depedency by using terminal class (as terminal.py or pyte)
  - Find many other cool stuff to add to my fabulous script ^^
