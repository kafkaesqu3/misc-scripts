if not exist "C:\windows\sysmon-config.xml" (
copy /z /y "\\jurassic.park\sysvol\jurassic.park\apps\sysmon\sysmon-config-master\sysmonconfig-export.xml" "C:\windows\"
)
 
sc query "Sysmon" | Find "RUNNING"
If "%ERRORLEVEL%" EQU "1" (
goto startsysmon
)
:startsysmon
net start Sysmon
 
If "%ERRORLEVEL%" EQU "1" (
goto installsysmon
)
:installsysmon
"\\jurassic.park\sysvol\jurassic.park\apps\sysmon\sysmon.exe" /accepteula -i c:\windows\config.xml