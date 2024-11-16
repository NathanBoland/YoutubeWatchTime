
from SpreadSheetInterface import *

import os
import shutil
import tempfile

import pyperclip

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller

import time
import psutil

# paths
original_profile_path = r"C:\Users\Nathan\AppData\Roaming\Mozilla\Firefox\Profiles\j4grchvt.default-release"

temp_profile_path = tempfile.mkdtemp()

shutil.copy(os.path.join(original_profile_path, "cookies.sqlite"), temp_profile_path)
shutil.copy(os.path.join(original_profile_path, "prefs.js"), temp_profile_path)
print("Copied profile")

# Driver initialisation
options = Options()
options.profile = temp_profile_path
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
print("Set preferences")

start_time = time.time()
print("Creating driver... ~6s")
driver = webdriver.Firefox(options=options)
print(f"Created driver - {time.time() - start_time:.2f}s")


driver.get("https://www.youtube.com/feed/history")