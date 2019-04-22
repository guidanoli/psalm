@echo off
if NOT "%1"=="" goto %1
:beggining
cls
echo.
echo 	Accepted commands:
echo. 
echo 	fc	cycle on Facebook (run many iterations)
echo 	fd	debug on Facebook (run only once)
echo 	g	generate Facebook SDK layer
echo 	md	make dictionary out of file
echo 	pc	cycle random phrase generation
echo 	pd	generate random phrase
echo 	r	remove all posts
echo 	sd	set settings to default
echo 	se	edit settings
echo 	sv	view settings
echo 	tc	show current token
echo 	td	delete token from list
echo 	tr	register (new) token in list
echo 	ts	select token from list
echo 	z	zip files to aws lambda
echo.

set /p i=" >>> "
goto %i%

:fc
echo.
set /p iterations=" #iterations = "
if %iterations% EQU 1 goto d
if %iterations% EQU 0 goto beggining
if %iterations% LSS 0 (
echo.
echo Invalid!
echo.
goto hold
)
echo.
echo from psalm import PsalmBot>_cycle.py
echo for i in range(%iterations%):>>_cycle.py
echo  print("Iteration #{} ---------------------".format(i+1))>>_cycle.py
echo  PsalmBot(0,0)>>_cycle.py
echo print("\nDone iterating %iterations% posts!\n")>>_cycle.py
python _cycle.py
del _cycle.py
goto hold

:fd
python -c "from psalm import PsalmBot; PsalmBot(0,0)"
goto hold

:g
if exist .\python rd /s /q .\python
if exist facebook-sdk-layer.zip del facebook-sdk-layer.zip
pip install facebook-sdk --target .\python
7z a -r -sdel facebook-sdk-layer.zip .\python
goto hold

:md
set /p input=" Input file [*.txt]: "
set /p output=" Output file (leave blank to copy input file's name) [*.dict]: "
echo from mngDictionaries import MakeDict>_mkdict_temp.py
echo dict = MakeDict("%input%","%output%")>>_mkdict_temp.py
echo if dict != None:>>_mkdict_temp.py
echo   print("Dictionary created successfully as "+dict+" ...\n")>>_mkdict_temp.py
python _mkdict_temp.py
del _mkdict_temp.py
goto hold

:tc
:td
:tr
:ts
echo from mngTokens import launch>_tkmng.py
echo launch("%i%")>>_tkmng.py
python _tkmng.py
del _tkmng.py
goto hold

:pc
set /p iterations=" #iterations = "
echo from mngSettings import getSetting>_prnt.py
echo from psalm import GetPhrase>>_prnt.py
echo for i in range(0,%iterations%):>>_prnt.py
echo  p=GetPhrase()>>_prnt.py
echo  if p != None:>>_prnt.py
echo   print(p+'\n')>>_prnt.py
echo --------------------------------------->_output.txt
echo %iterations% RANDOMLY GENERATED PHRASES>>_output.txt
echo --------------------------------------->>_output.txt
echo.>>_output.txt
python _prnt.py>>_output.txt
start _output.txt
del _prnt.py
goto hold

:pd
echo from mngSettings import getSetting>_prnt.py
echo from psalm import GetPhrase>>_prnt.py
echo p=GetPhrase()>>_prnt.py
echo if p != None:>>_prnt.py
echo   print(p)>>_prnt.py
echo --------------------------------------->_output.txt
echo RANDOMLY GENERATED PHRASE>>_output.txt
echo --------------------------------------->>_output.txt
echo.>>_output.txt
python _prnt.py>>_output.txt
start _output.txt
del _prnt.py
goto hold

:r
python remove.py
goto hold

:sd
:se
:sv
echo from mngSettings import launch>_stgsmng.py
echo launch("%i%")>>_stgsmng.py
echo.
python _stgsmng.py
del _stgsmng.py
goto hold

:z
if exist lambda.zip del lambda.zip
7z a -y lambda.zip psalm.py mngSettings.py *.cfg *.tk
goto hold

:hold
pause
if exist .\__pycache__ rd /s /q .\__pycache__
if exist .\_*.py del /q .\_*.py
if exist _output.txt del /q _output.txt
cls
goto beggining