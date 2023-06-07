# functions.py
import time
import os
import getpass
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

username = getpass.getuser()
driver_path = r"drivers\geckodriver.exe"
mozilla_profiles = r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles".format(username)
current_dir = os.path.dirname(os.path.abspath(__file__))
new_profile_directory = os.path.join(current_dir, "new_profile")

class ProfileHandler:
    def __init__(self):
        self.profiles_path = mozilla_profiles

    def get_profiles(self):
        profiles = os.listdir(self.profiles_path)
        return {"profiles": profiles}
    
    def profile_exists(self, profile_name):
        profile_path = os.path.join(self.profiles_path, profile_name)
        return os.path.exists(profile_path)
    def check_profile(self, profile_name):
        # Step 1: Extract profile name
        profile = profile_name.split("/")[-1]

        # Step 2: Check if the profile folder exists in the target directory
        target_directory = os.path.join(os.getcwd(), "new_profile")
        selected_profile_path = os.path.join(target_directory, profile)

        if not os.path.exists(selected_profile_path):
            # Copy the profile directory from the source path to the target directory
            source_directory = mozilla_profiles
            source_path = os.path.join(source_directory, profile)
            shutil.copytree(source_path, selected_profile_path)

        # Set GeckoDriver options
        geckodriver_options = FirefoxOptions()
        geckodriver_options.headless = False  # Set to True if you want to hide the browser window

        # Launch Firefox with GeckoDriver using the selected profile
        driver = webdriver.Firefox(
            executable_path=driver_path,
            options=geckodriver_options,
            firefox_profile=selected_profile_path
        )

        driver.get("https://mail.google.com")

        # Check if the profile is logged in or not
        if "Private and secure email at no cost" in driver.title:
            login_status = False
        else:
            login_status = True

        driver.quit()

        return {"profile": profile, "login_status": login_status}

def send_email(recipient, subject, body, selected_profiles):
    # ... Existing code for the send_email function ...
    if not os.path.exists(new_profile_directory):
        os.makedirs(new_profile_directory)

    selected_profile_directory = selected_profiles.split("\\")[-1]
    new_profile_path = os.path.join(new_profile_directory, selected_profile_directory)
    
 
    if not os.path.exists(new_profile_path):
        shutil.copytree(selected_profiles, new_profile_path)

    # Set GeckoDriver options
    geckodriver_options = webdriver.FirefoxOptions()
    geckodriver_options.headless = False  # Set to True if you want to hide the browser window

    # Launch Firefox with GeckoDriver
    driver = webdriver.Firefox(
        executable_path=driver_path,
        options=geckodriver_options,
        firefox_profile=new_profile_path
    )
    try :
        driver.get("https://mail.google.com/mail/u/0/#inbox?compose=new")
        time.sleep(5)
    except :
        print('page not opening ')
        driver.quit()
    # Wait for the recipient input field to be visible
    try :
        wait = WebDriverWait(driver, 10)
        recipient_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//div/input[@peoplekit-id="BbVjBd"]')))
        recipient_input.send_keys(recipient)
        time.sleep(1)
        recipient_input.send_keys(Keys.ESCAPE)
    except :
        print("recipient not valide")
        driver.quit()
    time.sleep(1)
    # subject
    try :
        subject_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="subjectbox"]')))
        subject_field.send_keys(subject)
        time.sleep(1)
    except :
        print("error subject")
        driver.quit()
    # body
    try :
        
        body_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@role="textbox"]')))
        body_field.send_keys(body)
    except :
        print("body email error")
        driver.quit()

    time.sleep(2)
    try:
        ActionChains(driver, 0.5).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
    except Exception as e:
        print(str(e))

    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="link_vsm"]')))
    except Exception as e:
        print(str(e))
        # Perform actions on the elements

    time.sleep(3)
    driver.quit()
