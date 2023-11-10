import subprocess

"""
Execute the other Python files in the project.
"""
# First, execute the SerialTestSpi.py file
subprocess.run(['python', '/home/censuspi/Py_core/SerialTestSpi.py'])

## Next, execute the SerialTestUart.py file
#subprocess.run(['python', '/home/censuspi/Py_core/SerialTestUart.py'])
