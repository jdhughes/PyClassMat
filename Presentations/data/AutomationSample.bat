rem ***Sample 02
cd ..\SWRSample02\
mf2005-swr_x64.exe SWRSample02.nam
mf2005-swr_x64.exe SWRSample02.02.nam
cd ..\Python\
python SWRSample02.py
python SWRSample02.02.py
python SWRSample02v.py
python SWRSample02v.02.py
rem ***Sample 16
cd ..\SWRTestSimulation16\
mf2005-swr_x64.exe SWRTestSimulation16.level.nam
mf2005-swr_x64.exe SWRTestSimulation16.tilted.nam
mf2005-swr_x64.exe SWRTestSimulation16.tilted.IC.nam
cd ..\python\
python SWRTestSimulation16.level.py
python SWRTestSimulation16.tilted.py
python SWRTestSimulation16.tilted.IC.py
rem END OF BATCH FILE
cd ..\
pause
