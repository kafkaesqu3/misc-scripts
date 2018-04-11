$interval=-5

Function Invoke-LogHarvest
[cmdletbinding()]
Param (
[string]$Provider,
[int]$EventId
   )
# End of Parameters
Process {
$results = Get-WinEvent -FilterHashTable @{Id=$EventId; LogName=$Provider; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
return $results
} # End of Process


'Microsoft-Windows-Sysmon/Operational'

$sysmon_events = Get-WinEvent -FilterHashTable @{LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)} 2>&1 | Out-Null
$sysmon_events | measure-object

$sysmon_process_create = Get-WinEvent -FilterHashTable @{Id=1; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_process_create | measure-object

$sysmon_file_create_time = Get-WinEvent -FilterHashTable @{Id=2; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_file_create_time | measure-object

$sysmon_network_connect = Get-WinEvent -FilterHashTable @{Id=3; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_network_connect | measure-object

$sysmon_process_terminate = Get-WinEvent -FilterHashTable @{Id=5; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_process_terminate | measure-object

$sysmons_driver_load = Get-WinEvent -FilterHashTable @{Id=6; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmons_driver_load | measure-object

$sysmon_image_load = Get-WinEvent -FilterHashTable @{Id=7; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_image_load | measure-object

$sysmon_create_remote_thread = Get-WinEvent -FilterHashTable @{Id=8; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_create_remote_thread | measure-object

$sysmon_create_file_create = Get-WinEvent -FilterHashTable @{Id=11; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_create_file_create | measure-object

$sysmon_registry_add_del = Get-WinEvent -FilterHashTable @{Id=12; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_registry_add_del | measure-object

$sysmon_registry_set = Get-WinEvent -FilterHashTable @{Id=13; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_registry_set | measure-object

$sysmon_registry_renamed = Get-WinEvent -FilterHashTable @{Id=14; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_registry_renamed | measure-object

$sysmon_file_stream = Get-WinEvent -FilterHashTable @{Id=15; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_file_stream | measure-object

$sysmon_pipe_create = Get-WinEvent -FilterHashTable @{Id=17; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_pipe_create | measure-object

$sysmon_pipe_connect = Get-WinEvent -FilterHashTable @{Id=18; LogName='Microsoft-Windows-Sysmon/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$sysmon_pipe_connect | measure-object

$security_events = Get-WinEvent -FilterHashTable @{LogName='Security';StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$security_events | measure-object

$winrm_events = Get-WinEvent -FilterHashTable @{LogName='Microsoft-Windows-WinRM/Operational'; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$winrm_events | measure-object

$wmi_events = Get-WinEvent -FilterHashTable @{LogName='Microsoft-Windows-WinRM/Operational';StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$wmi_events | measure-object

$process_creation_events = Get-Winevent -FilterHashTable @{ID=4688; LogName='Security';StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)}
$process_creation_events | measure-object
