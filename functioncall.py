import subprocess

class CallUSBdriver(object):
    def __init__(self, path='/home/censuspi/Py_core/USBdriver.py'):
        self.path = path
        
    def Call_python_file(self):
        subprocess.call(["python3", "{}".format(self.path)])
        
if __name__ == "__main__":
    c = CallUSBdriver()
    c.Call_python_file()