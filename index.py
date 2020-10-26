#!/usr/bin/python
import os
import sys
import json
import time
import importlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

templateTypes = {
    'follow_user_followers': 'FollowUserFollowers',
    'unfollow_following': 'UnfollowFollowing'
}

#Create storage dir structure if not exists
if not os.path.exists('storage'):
    os.makedirs('storage')
    open('storage/app.db', 'a').close()

    #Init db connection
    conn = sqlite3.connect('storage/app.db')
    db = conn.cursor()

    #Create followers table
    db.execute('''CREATE TABLE followers(
        id INTEGER PRIMARY KEY,
        user_name VARCHAR(45) NOT NULL,
        user_link VARCHAR(45) NOT NULL,
        followed INTEGER DEFAULT 0,
        followed_at VARCHAR(45),
        followed_back INTEGER,
        parent_account VARCHAR(45));''')
    db.execute('create unique index followers_unique on followers(user_name);')

    #Create cache table
    db.execute('CREATE TABLE cache(key VARCHAR(45), value VARCHAR(500), expiry VARCHAR(500))')
    db.execute('create unique index cache_unique on cache(key);')
    db.close()

#Get template
with open('settings.json', 'r') as settings:
    settings = json.load(settings)

    #Create chrome instance
    chromeOptions = webdriver.ChromeOptions()
    #chromeOptions.add_argument("--headless")
    chromeOptions.add_argument(f'disable-blink-features=AutomationControlled')
    chromeOptions.add_argument("user-data-dir=" + os.getcwd() + '/storage/Chrome')
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
    chromeOptions.add_argument(f'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36') 
    chromeOptions.add_experimental_option('prefs', { 'disk-cache-size': 4096 })
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options = chromeOptions)

    #Load twitter
    browser.get('https://twitter.com')

    #Wait until page loads
    try:
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='session[username_or_email]']")))
        if('home' not in browser.current_url):
            browser.find_element_by_css_selector("[name='session[username_or_email]']").send_keys(settings['username'])
            browser.find_element_by_css_selector("[name='session[password]']").send_keys(settings['password'])
            browser.find_element_by_css_selector("[data-testid='LoginForm_Login_Button']").click()
    except:
        print('Already logged in')

    #Run templates
    for template in settings['templates']:
        #Get the appropriate class
        templateType = template['type']
        templateInstance = importlib.import_module('src.templates.' + templateType)
        templateInstance = getattr(templateInstance, templateTypes[templateType])

        #Run the template
        templateInstance(template, browser).run()