$sLinkFile = "$env:USERPROFILE\Desktop\RS-LCE-Desktop.lnk" 
$sTargetFile = "$PSScriptRoot\run_app.bat" 
$sIconFile = "$PSScriptRoot\src\web\assets\icon.ico" # Icono oficial de RS
$WshShell = New-Object -ComObject WScript.Shell 
$Shortcut = $WshShell.CreateShortcut($sLinkFile) 
$Shortcut.TargetPath = $sTargetFile 
if (Test-Path $sIconFile) {
    $Shortcut.IconLocation = $sIconFile 
}
$Shortcut.WorkingDirectory = $PSScriptRoot 
$Shortcut.Save()
