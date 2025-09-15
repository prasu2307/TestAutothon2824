import datetime
import os
from utilities.readProperties import ReadConfig

tnow = datetime.datetime.now().strftime('%Y%m%d%H%M')
tstart = datetime.datetime.now()
# Read main configuration
environment = ReadConfig.get_env().lower()

allure_report_path = os.getcwd() + "\\Outputs\\Allure_reports"

python_file = os.getcwd() + '\\testCases\\test_facebook.py'
command = f'python -m pytest -s -v --disable-warnings -m ui_test2 --alluredir={allure_report_path} {python_file} --env="{environment}"'
print("command ", command)
os.system(command)

print('\nTime Elapsed: ', datetime.datetime.now() - tstart)
