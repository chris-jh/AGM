from libs.App import *
import sys

if (len(sys.argv)==2):
    app = App(sys.argv[1])
else:
    app = App()
