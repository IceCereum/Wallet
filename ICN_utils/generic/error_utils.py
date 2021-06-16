from inspect import getframeinfo, stack

def errormessage(cmd_shell, *strings, **kwargs):
    cmd_shell.perror("An error was encountered! Error Message:\n")

    cmd_shell.poutput("Configuration:")
    # TODO: add more metadata
    caller = getframeinfo(stack()[1][0])
    cmd_shell.poutput("File: " + caller.filename)
    cmd_shell.poutput("Func: " + caller.function)
    cmd_shell.poutput("Line: " + str(caller.lineno))

    exception = kwargs.get("exception", None)
    if exception:
        cmd_shell.poutput("\n")
        cmd_shell.poutput("Complete trace:")
        cmd_shell.poutput(exception)

    cmd_shell.poutput("\n")
    for i in strings:
        cmd_shell.poutput(i)

    escalated = kwargs.get("escalted", None)
    if escalated:
        cmd_shell.poutput("\nPlease send this Error Message to "               \
            "ns_raghav@hotmail.com and hope that I read your email in time.")

    return
