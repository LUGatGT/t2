
This is the t2 command line tool.
It provides a cli to t-square.

Notice:
This software is still alpha quality. I am not responsible if
it breaks anything. Use it at your own risk.

# Installation

Installation instructions:
t2 is written in python. It has only been tested with python3.
Although I think it should work with python2 as well.

You will need phantomjs for this project. You should be able
to install it using your distro's package manager.

`sudo apt-get install phantomjs`
            or
`sudo pacman -S phantomjs`
            or
etc

You should now use pip to install t2 and it's other dependencies.
Simply cd into the project directory and run:

`sudo pip install .`

You should then be able to run t2 from your command line.

Current supported commands:
`t2 --help`

# Hacking

If you make a modification to the code and would like to
see the changes you made avaible you can run:
`sudo pip install . --upgrade`

