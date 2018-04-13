
Function Invoke-LogHarvest ([string]$Provider, [string]$name, [int]$EventId)
{
	if ($PSBoundParameters.ContainsKey('EventId')) {
		$results = Get-WinEvent -FilterHashTable @{Id=$eventId; LogName=$Provider; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)} -erroraction 'silentlycontinue'
	}
	else 
	{
		$results = Get-WinEvent -FilterHashTable @{LogName=$Provider; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)} -erroraction 'silentlycontinue'
	}
	if ($results.Length -gt 0) {
		write-host $provider, $name, $results.length
		$returned.add($name)
	}
	return $results
}

#SYSMON
Function Harvest-AllLogs ([int]$interval=-5) {

	if ($interval -gt 0) {
		$interval = $interval * -1
	}
	
	$returned = New-Object -TypeName 'System.Collections.ArrayList';
	
	$ProcessCreate = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'ProcessCreate' -eventid 1
	$FileCreateTime = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'FileCreateTime' -eventid 2
	$NetworkConnect = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'NetworkConnect' -eventid 3
	$ProcessTerminate = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'ProcessTerminate' -eventid 5
	$DriverLoad = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'DriverLoad' -eventid 6
	$ImageLoad = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'ImageLoad' -eventid 7
	$CreateRemoteThread = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'CreateRemoteThread' -eventid 8
	$RawAccessRead = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'RawAccessRead' -eventid 9
	$ProcessAccess = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'ProcessAccess' -eventid 10
	$FileCreate = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'FileCreate' -eventid 11
	$RegistryEvent_Add= Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'RegistryEvent_Add' -eventid 12
	$RegistryEvent_Modify= Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'RegistryEvent_Modify' -eventid 13
	$RegistryEvent_Rename = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'RegistryEvent_Rename' -eventid 14
	$FileCreateStreamHash = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'FileCreateStreamHash' -eventid 15
	$PipeEvent_Create = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'PipeEvent_Create' -eventid 17
	$PipeEvent_Connect = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'PipeEvent_Connect' -eventid 18

	#OTHER
	$security_events = Invoke-LogHarvest -provider 'Security' -name 'security_events'

	$winrm_events = Invoke-LogHarvest -provider 'Microsoft-Windows-WinRM/Operational' -name 'winrm_events'

	$wmi_events = Invoke-LogHarvest -provider 'Microsoft-Windows-Wmi-Activity/Operational' -name 'wmi_events'

	$powershell_events = Invoke-LogHarvest -provider 'Microsoft-Windows-PowerShell/Operational' -name "powershell_events"

	$process_creation_events = Invoke-LogHarvest -provider 'Security' -name 'process_creation_events' -eventid 4688

	write-host DONE! $returned
}