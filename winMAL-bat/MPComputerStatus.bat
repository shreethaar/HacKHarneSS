@ECHO off
powershell -Command "& {if (Get-MPComputerStatus | where-object {$._RealTimeProtectionEnabled -like 'False'}) {write-host "property is false!"}}"
pause
