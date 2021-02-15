Public Function ShellRun(sCmd As String) As String

    'Run a shell command, returning the output as a string

    Dim oShell As Object
    Set oShell = CreateObject("WScript.Shell")

    'run command
    Dim oExec As Object
    Dim oOutput As Object
    Set oExec = oShell.Exec(sCmd)
    Set oOutput = oExec.StdOut

    'handle the results as they are written to and read from the StdOut object
    Dim s As String
    Dim sLine As String
    While Not oOutput.AtEndOfStream
        sLine = oOutput.ReadLine
        If sLine <> "" Then s = s & sLine & vbCrLf
    Wend

    ShellRun = s

End Function
