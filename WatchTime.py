######## READ ME OR YOUR FIREFOX MAY BREAK ########
# clone this directory if you're worried about stuffing up your profile and use that instead
# I did initially, then used my actual one and it lost a few things after trying to open a regular tab while testing ones were open
# It worked before I did this, so just dont open your regular browser while any testing tabs are open

# Ensure that sync is turned off for that b

shorts_to_time_constant = 0.78301

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
    def __init__(self, amtShorts, amtVideos, timeShorts, timeVideos, totalTime):
        self.amtShorts = amtShorts
        self.amtVideos = amtVideos
        self.timeShorts = timeShorts
        self.timeVideos = timeVideos
        self.totalTime = totalTime


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

# temp_profile_path = tempfile.mkdtemp()

# print("Copying and cleaning browser profile...")
# # Copy profile excluding unneeded folders
# for item in os.listdir(original_profile_path):
#     s = os.path.join(original_profile_path, item)
#     d = os.path.join(temp_profile_path, item)

#     # 'storage','shadercache'
#     if os.path.isdir(s) and item in ["storage"]:
#         continue
#     if os.path.isdir(s):
#         shutil.copytree(s, d, ignore=shutil.ignore_patterns("storage"))
#     else:
#         shutil.copy2(s, d)
# print(f"Copied profile - {time.time() - start_time:.2f}s")
# start_time = time.time()

# Driver initialisation
print("Setting Preferences... ~20s")
options = Options()
options.profile = original_profile_path
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
print(f"Set preferences - {time.time() - start_time:.2f}s")
start_time = time.time()
print("Creating driver... ~60s")
driver = webdriver.Firefox(options=options)
print(f"Created driver - {time.time() - start_time:.2f}s")
start_time = time.time()

wait = WebDriverWait(driver, 10)


def YouTube(daysToGet = 0):

    driver.get("https://www.youtube.com/feed/history")
    time.sleep(5)
    
    watchTime = WatchTime(0, 0, "", "", "")

    # Close any additional tabs that might have opened
    # for handle in driver.window_handles:
    #     driver.switch_to.window(handle)
    #     if "YouTube" not in driver.title:
    #         driver.close()

    # Switch back to the main YouTube tab
    # driver.switch_to.window(driver.window_handles[0])

    # Ensure we are on the YouTube history page
    # if driver.current_url != 'https://www.youtube.com/feed/history':
    #     driver.get('https://www.youtube.com/feed/history')
    #     time.sleep(10)

    print("Not on page")
    # driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + 'w')

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

    
    
    ytDays = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH, 
                "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer",
            )
        )
    )
    if ytDays:
        for ytDay in ytDays:
            # if ytDay.find_element(By.XPATH, "//*[@id=\"title\"]").text() != (date.today() - timedelta(days=2)).strftime("%A"):
            #     ytDays.remove(ytDay)
            print(ytDay.find_element(By.XPATH, "//*[@id=\"title\"]").text)
    else:
        print("No days found")
    
    try:
        # checks if youve watched anything today
        todayCheck = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "ytd-item-section-renderer.style-scope:nth-child(1) > div:nth-child(1) > ytd-item-section-header-renderer:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
                )
            )
        )
    except:
        print("No days found")
    else:
        if todayCheck.text == "Today":
            # print("Today found")
            # Shorts Counter
            time_shorts = 0
            try:
                # checks for shorts
                wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "ytd-item-section-renderer.style-scope:nth-child(1) > div:nth-child(3) > ytd-reel-shelf-renderer:nth-child(1) > div:nth-child(1)",
                        )
                    )
                )
            except:
                print("No shorts found")
            else:
                # print("Shorts found")
                try:
                    # presses the right arrow to load all shorts, only one press required because it loads all of them
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "#contents.style-scope.ytd-section-list-renderer ytd-item-section-renderer.style-scope.ytd-section-list-renderer div#contents.style-scope.ytd-item-section-renderer ytd-reel-shelf-renderer.style-scope.ytd-item-section-renderer div#contents.style-scope.ytd-reel-shelf-renderer yt-horizontal-list-renderer.style-scope.ytd-reel-shelf-renderer div#right-arrow.style-scope.yt-horizontal-list-renderer ytd-button-renderer.style-scope.yt-horizontal-list-renderer.arrow yt-button-shape button.yt-spec-button-shape-next.yt-spec-button-shape-next--text.yt-spec-button-shape-next--mono.yt-spec-button-shape-next--size-m.yt-spec-button-shape-next--icon-only-default.yt-spec-button-shape-next--enable-backdrop-filter-experiment",
                            )
                        )
                    ).click()
                    # print("More shorts found")
                except:
                    print("Less than 6 shorts found")
                shorts_div = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "#scroll-outer-container.style-scope.yt-horizontal-list-renderer div#scroll-container.style-scope.yt-horizontal-list-renderer div#items.style-scope.yt-horizontal-list-renderer",
                        )
                    )
                )
                time.sleep(3)

                # Locate the div and count the number of items
                no_shorts = len(
                    shorts_div.find_elements(
                        By.TAG_NAME, "ytm-shorts-lockup-view-model-v2"
                    )
                )
                watchTime.amtShorts = no_shorts
                time_shorts = no_shorts * shorts_to_time_constant

                print(f"Number of shorts watched: {no_shorts}")
                if time_shorts < 1:
                    watchTime.timeShorts = f"{time_shorts * 60:.2f}s"
                    print(f"Estimated time on shorts {time_shorts * 60:.2f}s")
                elif time_shorts < 60:
                    minutes = int(time_shorts)
                    seconds = int((time_shorts - minutes) * 60)
                    watchTime.timeShorts = f"{int(time_shorts)}m {int((time_shorts%1)*60)}s"
                    print(
                        f"Estimated time on shorts {int(time_shorts)}m {int((time_shorts%1)*60)}s"
                    )
                elif time_shorts >= 60:
                    watchTime.timeShorts = f"{int(time_shorts/60)}h {int(((time_shorts/60)%1)*60)}m {int((time_shorts%1)*60)}s"
                    print(
                        f"Estimated time on shorts {int(time_shorts/60)}h {int(((time_shorts/60)%1)*60)}m {int((time_shorts%1)*60)}s"
                    )

            # Video Counter

            # gets amount of videos
            video_div = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]'))
            )
            videos = video_div.find_elements(
                By.XPATH,
                "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-video-renderer",
            )
            # /html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-video-renderer[2]

            totalTime = 0
            watchedVideos = len(videos)
            watchTime.amtVideos = watchedVideos
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
                            int(video_length_parts[0].strip())
                            + (float(video_length_parts[1].strip()) / 60.0)
                        )
                    elif len(video_length_parts) == 3:
                        video_length = float(
                            (float(video_length_parts[0].strip()) * 60.0)
                            + int(video_length_parts[1].strip())
                            + (float(video_length_parts[2].strip()) / 60.0)
                        )
                    else:
                        print("something wrong")
                        print(video.get_attribute("class"))
                        print(video_length_parts)
                        print(video_percent)
                    # print(f"Time watched: {video_length * video_percent}")
                    totalTime += video_length * video_percent
                except:
                    # if that videos a current livestream or something
                    watchedVideos -= 1

            print(f"Number of videos watched: {watchedVideos}")

            # Time watching videos
            if totalTime < 1:
                watchTime.timeVideos = f"{totalTime * 60:.2f}s"
                print(f"Time watching videos: {totalTime * 60:.2f}s")
            elif totalTime < 60:
                minutes = int(totalTime)
                seconds = int((totalTime - minutes) * 60)
                watchTime.timeVideos = f"{int(totalTime)}m {int((totalTime%1)*60)}s"
                print(
                    f"Time watching videos: {int(totalTime)}m {int((totalTime%1)*60)}s"
                )
            elif totalTime >= 60:
                watchTime.timeVideos = f"{int(totalTime/60)}h {int(((totalTime/60)%1)*60)}m {int((totalTime%1)*60)}s"
                print(
                    f"Time watching videos: {int(totalTime/60)}h {int(((totalTime/60)%1)*60)}m {int((totalTime%1)*60)}s"
                )

            # Total Time
            totalTime += time_shorts
            if totalTime < 1:
                watchTime.totalTime = f"{totalTime * 60:.2f}s"
                print(f"\nTotal YouTube Time: {totalTime * 60:.2f}s")
            elif totalTime < 60:
                minutes = int(totalTime)
                seconds = int((totalTime - minutes) * 60)
                watchTime.totalTime = f"{int(totalTime)}m {int((totalTime%1)*60)}s"
                print(
                    f"\nTotal YouTube Time: {int(totalTime)}m {int((totalTime%1)*60)}s"
                )
            elif totalTime >= 60:
                watchTime.totalTime = f"{int(totalTime/60)}h {int(((totalTime/60)%1)*60)}m {int((totalTime%1)*60)}s"
                print(
                    f"\nTotal YouTube Time: {int(totalTime/60)}h {int(((totalTime/60)%1)*60)}m {int((totalTime%1)*60)}s"
                )

        else:
            print("No videos watched today")
            
    return watchTime


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


SpreadSheet()
daysToGet = getLatestYtEntry()

watchTime = YouTube(daysToGet)

SpreadSheet()
setWatchTime(watchTime)




temp_profile_path = None

# shutil.rmtree(temp_dir)

driver.quit()
quit()
