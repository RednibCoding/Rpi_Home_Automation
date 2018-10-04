
# use this script to debug your android device while running the app
# Developer options and USB-debugging have to be enabled on the device
# also adb has to be installed on the dev machine (ubuntu: sudo apt-get install adb)
#
# you can edit grep tags to change the output (currently, only python errors
# and their occurence will be displayed)

import os
os.system("adb shell logcat | grep -E 'Traceback|File '")
