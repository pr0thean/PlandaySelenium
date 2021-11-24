To run following test with a use of Selenium + python:

Requirements before test run:
+ Install Python 3.7 /Pycharm, detailed description how to do it please find below following link: https://phoenixnap.com/kb/how-to-install-python-3-windows
+ Once python is installed, install following packeges by using command pip:

pip install numpy
pip install selenium
pip install pytest
+ Install Chromedriver.exe from the following website: https://chromedriver.chromium.org/
+ In directory: testrun_config/config.ini change executable_path for the path where your webdriver is located
+ In following directory tests/test_schedule_section/user_accounts fill username_correct and password_correct value with credentials
+ to run test type from you project directory terminal: pytest -> test should start run 
+ output in the console should be the same as shown in the logs_from_test_run.PNG file


Structure of the files:

plan_day/ -> here you can find all pages connected with running test

testrun_config/ -> inside this folder there is config file where you should put at least path to your webdriver location

tests/test_schedule_section/ -> here is the main test with user_account file
