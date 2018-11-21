import os
import pathlib
print (os.getcwd())
print (os.path.join(os.getcwd(), r'../DataSync/datasync/config/'))
path = pathlib.Path(__file__).absolute().parent.parent
print(path)
