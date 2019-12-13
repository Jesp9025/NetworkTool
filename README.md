# GUI-Project
The task is to make a GUI-based program.
#
We are making a Network Helping Tool.

#    
Made by Jesper, Julius, Mantas & Erki
#
# Features
- Ping
- Traceroute
- Flush DNS
- Custom Command
- Whois Lookup
- Port Scanner
- Music Player
- Subnet Calculator
- CPU Usage Monitor

# Dependencies
python-whois

pygame

pysimplegui

psutil

# Bugs
- Decoding of text not working on machines with specific languages
- Whois output is not as pretty as wanted

# Bugfixes
- Crashed on music play if you played directly with "Python". Running directly with Python would set working directory to SYSTEM32, and song could not be found. Added path to file into a variable, in order to get directory of sound files, no matter how you run the program.
 Not an absolute path.. Dont worry.
