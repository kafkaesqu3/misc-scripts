
Function Invoke-LogHarvest ([string]$Provider, [string]$name, [int]$EventId)
{
		write-host $provider

	if ($PSBoundParameters.ContainsKey('EventId')) {
		$results = Get-WinEvent -FilterHashTable @{Id=$eventId; LogName=$Provider; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)} -erroraction 'silentlycontinue'
	}
	else 
	{
		write-host "No id specified!"
		$results = Get-WinEvent -FilterHashTable @{LogName=$Provider; StartTime=((Get-Date).AddMinutes($interval)); EndTime=(Get-Date)} -erroraction 'silentlycontinue'
	}
	if ($results.Length -gt 0) {
		write-host $provider, $name, $results.length
		$returned.add($name)
	}
	return $results
}


Function Harvest-AllLogs ([int]$interval=-5) {

	if ($interval -gt 0) {
		$interval = $interval * -1
	}
	
	$returned = New-Object -TypeName 'System.Collections.ArrayList';
	#SYSMON	
	$global:ProcessCreate = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'ProcessCreate' -eventid 1
	$global:FileCreateTime = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'FileCreateTime' -eventid 2
	$global:NetworkConnect = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'NetworkConnect' -eventid 3
	$global:ProcessTerminate = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'ProcessTerminate' -eventid 5
	$global:DriverLoad = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'DriverLoad' -eventid 6
	$global:ImageLoad = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'ImageLoad' -eventid 7
	$global:CreateRemoteThread = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'CreateRemoteThread' -eventid 8
	$global:RawAccessRead = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'RawAccessRead' -eventid 9
	$global:ProcessAccess = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'ProcessAccess' -eventid 10
	$global:FileCreate = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'FileCreate' -eventid 11
	$global:RegistryEvent_Add= Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'RegistryEvent_Add' -eventid 12
	$global:RegistryEvent_Modify= Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'RegistryEvent_Modify' -eventid 13
	$global:RegistryEvent_Rename = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'RegistryEvent_Rename' -eventid 14
	$global:FileCreateStreamHash = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'FileCreateStreamHash' -eventid 15
	$global:PipeEvent_Create = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'PipeEvent_Create' -eventid 17
	$global:PipeEvent_Connect = Invoke-LogHarvest -provider 'Microsoft-Windows-Sysmon/Operational' -name 'PipeEvent_Connect' -eventid 18

	#OTHER
	$global:security_events = Invoke-LogHarvest -provider 'Security' -name 'security_events'
	$global:system_events = Invoke-LogHarvest -provider 'System' -name 'system_events'

	$global:winrm_events = Invoke-LogHarvest -provider 'Microsoft-Windows-WinRM/Operational' -name 'winrm_events'

	$global:wmi_events = Invoke-LogHarvest -provider 'Microsoft-Windows-Wmi-Activity/Operational' -name 'wmi_events'

	$global:powershell_events = Invoke-LogHarvest -provider 'Microsoft-Windows-PowerShell/Operational' -name "powershell_events"

	$global:process_creation_events = Invoke-LogHarvest -provider 'Security' -name 'process_creation_events' -eventid 4688

	write-host DONE! $returned
}
