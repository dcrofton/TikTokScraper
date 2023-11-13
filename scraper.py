#!/usr/bin/env python3
import requests
import json
import time
import random
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
from datetime import datetime, date, timedelta

options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = Driver(uc=True)

timers = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
]
variables = [
    "https://www.tiktok.com/login/phone-or-email/email", "//input[@placeholder='Email or username']",
    "//input[@placeholder='Password']", "//button[@type='submit']"
]

with open('user.txt') as f:
    line = f.readlines()
username = line[0][10:-1]
password = line[1][10:-1 ]

start_b = time.time()
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

def sleeper():
        time.sleep(float("0." + random.choice(timers[0:3]) + random.choice(timers[0:4]) + random.choice(timers[0:9])))

def logging_in():
        try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, variables[1])))
                fieldForm = driver.find_element("xpath", variables[1])
        except:
                driver.quit()
        finally:
                for i in username:
                        fieldForm.send_keys(i)
                        sleeper()

        fieldForm = driver.find_element("xpath", variables[2])
        for i in password:
                fieldForm.send_keys(i)
                sleeper()

        try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, variables[3])))
        except:
                driver.quit()
        finally:
                button = driver.find_element("xpath", variables[3])
                button.click()

driver.get(variables[0])
if len(username) != 0 and len(password) != 0:
    logging_in()
end = time.time()
input("Press Enter to continue...")

url = 'https://www.tiktok.com/search/video?q=fashion&t=1699558711587'

driver.get(url)

for i in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

content = BeautifulSoup(driver.page_source, "lxml")
postArray = []
postViewCounts = []
for post in content.find_all('div', attrs={"class": 'tiktok-1as5cen-DivWrapper e1cg0wnj1'}):
    for tag in post:
        if tag.has_attr("href"):
            if len(tag['href']) != 0:
                postArray.append(tag['href'])
for tag in content.find_all('div', attrs={"class": 'tiktok-1lbowdj-DivPlayIcon etrd4pu4'}):
    postViewCounts.append(tag.text)

date_pattern = re.compile(r'\d{4}-\d{1,2}-\d{1,2}|\d{1,2}-\d{1,2}|\d+d ago')
days_ago_pattern = re.compile(r'\d+d ago')
objectList = []
print(len(postArray))
for i in range(len(postArray)):
    post = postArray[i]
    print(post)
    driver.get(post)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    content = BeautifulSoup(driver.page_source, "lxml")
    caption = ""
    hashtags = ""
    comments = "["
    for tag in content.find_all(attrs={"class": ['tiktok-j2a19r-SpanText efbd9f0', 
                                                 'ejg0rhn6 tiktok-g8ml1x-StyledLink-StyledCommonLink er1vbsz0']}):
        if tag.text != " ":
            caption = caption + tag.text
        if '#' in tag.text:
            hashtags = hashtags + tag.text
    for tag in content.find_all(attrs={"class": 'tiktok-13revos-DivCommentListContainer ekjxngi3'}):
        for comment in tag:
            text = date_pattern.split(comment.text)[0]
            if comments == "[":
                comments = comments + text
            else:
                comments = comments + "," + text
    comments = comments + ']'
    date_posted = ""
    for tag in content.find_all(attrs={"class": 'tiktok-31630c-DivInfoContainer e17fzhrb0'}):
        for component in tag:
            text = component.text.split(' · ')[-1]
            if len(text) != 0 and text != "Follow":
                print(text)
                if bool(days_ago_pattern.match(text)):
                    days_to_subtract = int(text.split('d')[0])
                    date_posted = datetime.now() - timedelta(days=days_to_subtract)
                    date_posted = date_posted.strftime("%m/%d/%Y")
                else:
                    nums = text.split('-')
                    if len(nums) == 2:
                        date_posted = "{m}/{d}/2023".format(m=nums[0], d=nums[1])
                    else:
                        date_posted = "{m}/{d}/{y}".format(m=nums[1], d=nums[2], y=nums[0])
    account = content.find('span', attrs={"class": 'tiktok-1c7urt-SpanUniqueId evv7pft1'}).text
    like_count = content.find('strong', attrs={"data-e2e": 'like-count'})
    saved_count = content.find('strong', attrs={"data-e2e": 'undefined-count'})
    if like_count and saved_count:
        postObject = {
            'Post URL': post,
            'Account': account,
            'Views': postViewCounts[i],
            'Likes': like_count.text,
            'Comments': comments,
            'Saved': saved_count.text,
            'Caption': caption,
            'Hashtags': hashtags,
            'Date Posted': date_posted,
            'Date Collected': (date.today()).strftime("%m/%d/%y")
        }
        objectList.append(postObject)

driver.quit()

with open('TikTokFashionData.csv', 'w') as file:
    fieldnames = ['Post URL','Account','Views', 'Likes', 'Comments',
                  'Saved', 'Caption', 'Hashtags', 'Date Posted', 'Date Collected']
    writer = csv.writer(file)
    writer.writerow(fieldnames)
    for postObject in objectList:
        writer.writerow(postObject.values())