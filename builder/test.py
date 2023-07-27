import subprocess

command = "python3 texliveonfly.py -c pdflatex resume.tex"
# a = subprocess.run(command.split(),shell=True,capture_output=True)
# print(a.returncode)
# print(a.stdout.decode())
# print(a.stderr.decode())

# command = 'python3 texliveonfly.py -c pdflatex resume.tex;'
# a = subprocess.run(command.split(),shell=True,capture_output=True)
# if a.returncode != 0:
#     print("error: ",a.stderr.decode())
# else:
#     print("success: ",a.stdout.decode())

output = subprocess.Popen(command, shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
success, error = output.communicate()

if success:
    print("success: ", success)
else:
    print("error: ", error)
# .stdout.read().decode('utf-8').strip()  # type: ignore
