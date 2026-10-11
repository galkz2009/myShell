echo off
rem hexdump.bat opens the given file and shows its hexadecimal representation
set target=%1
python %~dp0\\hexdump.py %target%
