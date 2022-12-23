# RDG2CSV v1.02
*.rdg to .json / .rdg to .csv / .rdg to .ahk*

## About:

Don't let the name fool you, this script will export your .RDG file into 3 files: .JSON, .CSV and .AHK

First it will export a .JSON file which makes it easier for the script to process. Then it will push out a .CSV file that makes the .RDG file human readable, perfect if you need to make inventory of your servers in a Excel file. After that, it will create a AHK hotstrings script, this is the true purpose of this script!

With the AHK hotstrings script you will be able to to type any IP and get required data out of that IP. It currently supports 6 functions:

---

### 1. ${IP} => Server Name / Group Subgroup @ IP
> $192.168.0.80 =>
> AlphaServer / BravoGroup CharlieSubGroup @ 192.168.0.80

### 2. $n{IP} => Server Name
> $n192.168.0.80 =>
> AlphaServer

### 3. $u{IP} => Server Username
> $u192.168.0.80 =>
> ServerAdmin

### 4. $u@{IP} => Server UserName @ IP
> $u@192.168.0.80 =>
> ServerAdmin@192.168.0.80

### 5. ${SERVERNAME} => Server Name / Group Subgroup @ IP
> $AlphaServer =>
> AlphaServer / BravoGroup CharlieSubGroup @ 192.168.0.80

### 6. $ip{SERVERNAME} => Server IP
> $ipAlphaServer =>
> 192.168.0.80

---

Of course, in order for this script to work as intended, your servers in RCMan should contain all of the information as complete as possible.

Note: This script currently only reaches server in max a sub level. ex.
> Group > SubGroup > Server

Also, this script has only been tested with .RDG files exported from RDCMan v2.90.

## Installation:

This script was written in Python 3.11, therefore it is required you have Python installed.

Clone this repository to a desired folder in your machine.

The script dependencies are included in the requirements.txt file, you can install these by simply running this command in the scripts root folder:
> pip install -r requirements.txt

Of course, it is recommended you use a virtual environment if you develop stuff in Python, but that is outside the scope of this installation guide.

If you wish to use the AHK hotstrings script, you will need to install AHK: https://www.autohotkey.com/

## Running the Script:

Drop the .RDG file exported from RDCMan into the scripts input folder.

Run RDG2CSV.py

Your .JSON, .CSV and .AHK files will be exported into ./output

## Running the AHK hotstrings script at Windows StartUp:

Create a Desktop Shortcut of the server.ahk script. Hit "Windows Key + R" and type:
>shell:startup

Move the Scripts Desktop Shortcut to the Startup folder.