import subprocess

def runSystemCommad(command: str):
    """run the system command and return the output, error and execution object """
    output = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output.communicate(), output
