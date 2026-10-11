echo off
rem hexdump.bat opens the given file and shows its hexadecimal representation
set target=%1
set pattern=%2
python %~dp0\\grep.py %target% %pattern%
