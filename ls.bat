echo off
rem ls.bat shows a list of files and diretories at the target folder
set target=%1
python %~dp0\\ls.py %target%
