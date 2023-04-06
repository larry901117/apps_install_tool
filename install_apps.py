#Version 1.0.1
#1. trigger "Stay awake" before workflow to prevent screen shutdown
#2. fixed print log "count" to correct number


import uiautomator2
import subprocess
import re
import time
import datetime

WAIT_TIME = 5
STORE_COMMAND = "adb shell am start -a android.intent.action.VIEW -d market://details?id="
SCREENSHOT_COMMAND = "adb shell screencap -p /sdcard//Pictures/Screenshots/screencap_"
CREATE_FOLDER_COMMAND = "adb shell mkdir "
UI_INIT_COMMAND = "python -m uiautomator2 init"
GREP_PACKAGE_COMMAND = "adb shell 'pm list packages -f' | grep "
STAY_AWAKE_COMMAND = "adb shell settings put global stay_on_while_plugged_in 3"

def adb_devices():
	result = subprocess.check_output(["adb","devices"],shell=False)
	match = re.findall("([^\s]+)\s+device(?!s)", result.decode("utf-8"), re.M)
	print(match)


def get_data(path):
	with open(path) as f:
		data = []
		for line in f.readlines():
			data.append(line.strip())
	return data

def install_apps(dut,packages):
	filename = str(datetime.date.today()) + "_not_installed_packages.txt"
	count = 1
	total = len(packages)
	subprocess.run(STAY_AWAKE_COMMAND,shell=True)
	#subprocess.run(CREATE_FOLDER_COMMAND+"/sdcard//Pictures/Screenshots/",shell=True)
	with open(filename,'w') as txt:
		for package in packages:
			subprocess.run(STORE_COMMAND+package,shell=True)
			print("count:"+str(count)+", total:"+str(total))
			try:
				dut(text = "Install").click()
			except:
	  			print("Failed on "+package)

			count = count + 1
			time.sleep(WAIT_TIME)
			#subprocess.run(SCREENSHOT_COMMAND+package+".png",shell=True)
			try:
				return_data = subprocess.check_output(GREP_PACKAGE_COMMAND+package,shell=True)
				if return_data == "":
					txt.write(package+"\n")
			except:
				txt.write(package+"\n")		
				




if __name__ == '__main__':
	packages = get_data('package_name.txt')
	sn_list = adb_devices()
	subprocess.run(UI_INIT_COMMAND,shell = True)
	dut = uiautomator2.connect(sn_list)
	install_apps(dut,packages)
