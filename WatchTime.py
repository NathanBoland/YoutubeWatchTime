######## READ ME OR YOUR FIREFOX MAY BREAK ########
# clone this directory if you're worried about stuffing up your profile and use that instead
# I did initially, then used my actual one and it lost a few things after trying to open a regular tab while testing ones were open
# It worked before I did this, so just dont open your regular browser while any testing tabs are open

# Ensure that sync is turned off for that b

shorts_to_time_constant = 0.78301 * 60

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

class WatchTime:
    def __init__(self, date, amtShorts, amtVideos, timeVideos):
        self.date = date
        self.amtShorts = amtShorts
        self.amtVideos = amtVideos
        self.timeVideos = timeVideos
    
    def __add__(self, other):
        return WatchTime(self.date, self.amtShorts + other.amtShorts, self.amtVideos + other.amtVideos, self.timeVideos + other.timeVideos)
    
    def print_details(self):
        print(f"Date: {self.date}  - ")
        print(f"Shorts: {self.amtShorts} - ")
        print(f"Videos: {self.amtVideos} - ")
        print(f"Video Time: {self.timeVideos}")
        print("\n")


start_time = time.time()

# Check if Firefox is running and terminate it
# for process in psutil.process_iter(["pid", "name"]):
#     if process.info["name"] == "firefox.exe":
#         os.kill(process.info["pid"], 9)
#         print(f"Terminated Firefox process with PID: {process.info['pid']}")


start_time = time.time()
# paths
if os.name == "posix":
    original_profile_path = "/Users/nathan/Library/Application Support/Firefox/Profiles/bn3d7uvb.default-release-1"
elif os.name == "nt":
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

wait = WebDriverWait(driver, 10)

def toDate(ytObj = webdriver.Firefox._web_element_cls):
    dateString = ytObj.find_element(By.CSS_SELECTOR, "div:nth-child(1) > ytd-item-section-header-renderer:nth-child(1) > div:nth-child(1) > div:nth-child(1)").text
    
    if dateString == "Today":
        return date.today()
    elif dateString == "Yesterday":
        return date.today() - timedelta(days=1)
    elif dateString == (date.today() - timedelta(days=2)).strftime("%A"):
        return date.today() - timedelta(days=2)
    elif dateString == (date.today() - timedelta(days=3)).strftime("%A"):
        return date.today() - timedelta(days=3)
    elif dateString == (date.today() - timedelta(days=4)).strftime("%A"):
        return date.today() - timedelta(days=4)
    elif dateString == (date.today() - timedelta(days=5)).strftime("%A"):
        return date.today() - timedelta(days=5)
    elif dateString == (date.today() - timedelta(days=6)).strftime("%A"):
        return date.today() - timedelta(days=6)
    elif len(dateString)  <= 4:
        raise ValueError("Too short/no date string provided")
    elif len(dateString) <= 6:
        # Format is "Short-Month Day - Jan 2
        parsed_date = time.strptime(f"{dateString} {date.today().year}", "%b %d %Y")
        return datetime(*parsed_date[:6]).date()
    elif len(dateString) <= 11:
        # Format is "Month Day Year - January 2 2024
        parsed_date = time.strptime(dateString, "%B %d %Y")
        return datetime(*parsed_date[:6]).date() 
    else:
        raise ValueError("Too long date string provided")
        
            
            
        


def YouTube(daysToGet = 0):
    
    oldestDate = date.today() - timedelta(days=daysToGet)
    print(f"Oldest date to get: {oldestDate.strftime('%d-%m-%Y')}")

    driver.get("https://www.youtube.com/feed/history")
    time.sleep(5)

    print(f"Opened YouTube - {time.time() - start_time:.2f}s")
    # tries to press the sign up button to initiate a login, most of the time it logs in automatically but sometimes not
    try:
        driver.find_element(
            By.CSS_SELECTOR,
            "html body ytd-app div#content.style-scope.ytd-app ytd-page-manager#page-manager.style-scope.ytd-app ytd-browse.style-scope.ytd-page-manager ytd-two-column-browse-results-renderer.style-scope.ytd-browse.grid.grid-6-columns div#primary.style-scope.ytd-two-column-browse-results-renderer ytd-section-list-renderer.style-scope.ytd-two-column-browse-results-renderer div#contents.style-scope.ytd-section-list-renderer ytd-item-section-renderer.style-scope.ytd-section-list-renderer div#contents.style-scope.ytd-item-section-renderer ytd-message-renderer.style-scope.ytd-item-section-renderer div#message-button.style-scope.ytd-message-renderer ytd-button-renderer.style-scope.ytd-message-renderer yt-button-shape a.yt-spec-button-shape-next.yt-spec-button-shape-next--outline.yt-spec-button-shape-next--call-to-action.yt-spec-button-shape-next--size-m.yt-spec-button-shape-next--icon-leading.yt-spec-button-shape-next--enable-backdrop-filter-experiment",
        ).click()
        print("Sign up button pressed\n")
    except:
        print(f"")

    """
    Psuedo Code
    call yt function with noDays to get
    convert noDays into the last date needed to get
    
    while last date newer than oldestYtDate
        scroll down
        get all days
        get oldestYtDate
    
    for all days
        press right arrow to load all shorts
    for all days
        calculate watch time for shorts
        calculate watch time for videos
        update list with watch time object
    return list
    
    """
    ytDays = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH, 
                "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer",
            )
        )
    )
    ytOldestDate = toDate(ytDays[-1])

    while oldestDate <= ytOldestDate:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        
        # wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{len(ytDays)+1}]")))
        time.sleep(3)
        ytDays = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH, 
                    "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer",
                )
            )
        )
        ytOldestDate = toDate(ytDays[-1])
        
        
    for i in range(len(ytDays)):
        print(f"Day {i + 1}")
        try:
            driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{i + 1}]/div[3]/ytd-reel-shelf-renderer/div[2]/yt-horizontal-list-renderer/div[3]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]").click()
            print("Found more Shorts")
        except:
            print("Less than 6 shorts found")
    
    ytDays = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH, 
                "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer",
            )
        )
    )
    
    allDays = []
    
    for ytDay in ytDays:
        print(toDate(ytDay).strftime("%d-%m-%Y"))
        
        dayWatchTime = WatchTime(toDate(ytDay), 0, 0, 0)
        
        # Shorts Counter
        try:
            # checks for shorts
            shorts_div =  ytDay.find_element(By.CSS_SELECTOR, "div:nth-child(3) > ytd-reel-shelf-renderer:nth-child(1) > div:nth-child(2) > yt-horizontal-list-renderer:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)")
        except:
            print("No shorts found")
        else:
            # shorts_div = ytDay.find_element(By.CSS_SELECTOR, "div:nth-child(3) > ytd-reel-shelf-renderer:nth-child(1) > div:nth-child(2) > yt-horizontal-list-renderer:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)")

            # Locate the div and count the number of items
            no_shorts = len(
                shorts_div.find_elements(
                    By.TAG_NAME, "ytm-shorts-lockup-view-model-v2"
                )
            )
            dayWatchTime.amtShorts = no_shorts
            print(f"Number of shorts watched: {no_shorts}")

        # Video Counter

        # gets amount of videos
        videos = ytDay.find_elements(
            By.TAG_NAME,
            "ytd-video-renderer",
        )
        print(f"length of videos: {len(videos)}")
        watchedVideos = len(videos)
        totalTime = 0
        for video in videos:

            # gets video percent as int
            try:
                video_percent = video.find_element(
                    By.CSS_SELECTOR,
                    "#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail div#overlays.style-scope.ytd-thumbnail ytd-thumbnail-overlay-resume-playback-renderer.style-scope.ytd-thumbnail div#progress.style-scope.ytd-thumbnail-overlay-resume-playback-renderer",
                ).get_attribute("style")
                video_percent = (
                    int(video_percent.split(" ")[1].split("%")[0]) / 100.0
                )

                # attempts to get length
                video_length_text = (
                    video.find_element(By.CLASS_NAME, "badge-shape-wiz__text")
                    .get_attribute("textContent")
                    .strip()
                )
                # print(f"Raw video length text: {video_length_text}")

                video_length_parts = video_length_text.split(":")
                # print(f"Video length parts: {video_length_parts}")

                # some videos have hours
                if len(video_length_parts) == 2:
                    video_length = float(
                        (float(video_length_parts[0].strip()) * 60.0)
                        + (float(video_length_parts[1].strip()))
                    )
                elif len(video_length_parts) == 3:
                    video_length = float(
                        (float(video_length_parts[0].strip()) * 60.0 * 60.0)
                        + (float(video_length_parts[1].strip()) * 60.0)
                        + (float(video_length_parts[2].strip()))
                    )
                else:
                    print("something wrong")
                    print(video.get_attribute("class"))
                    print(video_length_parts)
                    print(video_percent)
                # print(f"Time watched: {video_length * video_percent}")
                totalTime += video_length * video_percent
            except Exception as e:
                print(f"Error: {e}")
                # if that videos a current livestream or something
                watchedVideos -= 1

        print(f"Number of videos watched: {watchedVideos}")
        dayWatchTime.amtVideos = watchedVideos

        # Time watching videos
        dayWatchTime.timeVideos = totalTime
        
        # add to list, if the date is the same as any other day, add the times together
        
        if len(allDays) == 0:
            allDays.append(dayWatchTime)
        else:
            for i in range(len(allDays)):
                if allDays[i].date == dayWatchTime.date:
                    allDays[i] += dayWatchTime
                    break
                elif i == len(allDays) - 1:
                    allDays.append(dayWatchTime)

        # # Total Time
        # totalTime += time_shorts
        # if totalTime < 1:
        #     dayWatchTime.totalTime = f"{totalTime * 60:.2f}s"
        #     print(f"\nTotal YouTube Time: {totalTime * 60:.2f}s")
        # elif totalTime < 60:
        #     minutes = int(totalTime)
        #     seconds = int((totalTime - minutes) * 60)
        #     dayWatchTime.totalTime = f"{int(totalTime)}m {int((totalTime%1)*60)}s"
        #     print(
        #         f"\nTotal YouTube Time: {int(totalTime)}m {int((totalTime%1)*60)}s"
        #     )
        # elif totalTime >= 60:
        #     dayWatchTime.totalTime = f"{int(totalTime/60)}h {int(((totalTime/60)%1)*60)}m {int((totalTime%1)*60)}s"
        #     print(
        #         f"\nTotal YouTube Time: {int(totalTime/60)}h {int(((totalTime/60)%1)*60)}m {int((totalTime%1)*60)}s"
        #     )
        """
        remove all days after the last day
        check the sequence of the days
            add in any missing days with blank values
        remove current day if it exists
        """
        for i in range(len(allDays)):
            if i == 0:
                continue # skip the first day
            if allDays[i].date != allDays[i-1].date - timedelta(days=1): # if the current day is not the day before
                allDays.insert(i, WatchTime(allDays[i-1].date - timedelta(days=1), 0, 0, 0)) # add in a blank day
                
        
        
        for i in range(len(allDays) - 1, -1, -1):
            if allDays[i].date <= oldestDate:
                allDays.pop(i)
        
        

        if allDays[0].date == date.today():
            allDays.pop(0)
        
        
    print("\n\n-----------------------------------\n\n")
    for day in allDays:
        print(f"Date: {day.date.strftime('%d-%m-%Y')}")
        print(f"Shorts: {day.amtShorts}")
        print(f"Videos: {day.amtVideos}")
        print(f"Video Time: {day.timeVideos}")
        print("\n")
    return allDays


def SpreadSheet():
    print("going to doc page")
    driver.get(
        "https://docs.google.com/spreadsheets/d/1f4E283QHxm8aUjfBSD-DgNlR6VO-dmu-/edit?gid=441154842#gid=441154842"
    )
    time.sleep(5)

    # wait for spreadsheet to load
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[4]/div/div[2]/div/div[5]/div[2]/div[1]/div[2]")
        )
    )

    # get spreadsheet element
    try:
        sheet = driver.find_element(
            By.XPATH, "/html/body/div[4]/div/div[2]/div/div[5]/div[2]/div[1]/div[2]"
        )
    except:
        print("Could not find Spreadsheet")


# Run Sequence
"""
Init sheet
find latest yt entry, and how many entries missing
run yt function with missing entries


"""

SpreadSheet()
daysToGet = getLatestYtEntry()

daysWatchTime = YouTube(daysToGet)

SpreadSheet()
getLatestYtEntry()
goAmt(1, "Up")
for day in daysWatchTime:
    timeShorts = day.amtShorts * shorts_to_time_constant
    setWatchTime(day.timeVideos + timeShorts, day.amtShorts, timeShorts, day.amtVideos, day.timeVideos)




temp_profile_path = None
driver.quit()
quit()
