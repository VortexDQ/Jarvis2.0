REM Jarvis AI Assistant - Silent Launcher
REM This VBScript runs Jarvis in the background without showing a command window

Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
batchFile = objFSO.BuildPath(scriptPath, "run_jarvis.bat")

' Run the batch file silently (0 = hidden window, true = wait for process)
objShell.Run batchFile, 0, False

' Exit silently
WScript.Quit 0
