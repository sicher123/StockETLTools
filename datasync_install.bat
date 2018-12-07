cd %~dp0
python setup.py install
echo "@echo off ^ start python %~dp0\DataSync\datasync\sync\guojin_sync.py ^ exit">hdf5Sync.bat
schtasks  /create  /tn  hdf5_sync /tr hdf5Sync.bat /sc  DAILY /st  00:00:00 /et 01:00:00 /mo 2 /ri 59
echo "datasync install finished"