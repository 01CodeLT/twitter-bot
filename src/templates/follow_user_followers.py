import time
from src.db import DB
from src.utils import Utils
from random import randrange
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FollowUserFollowers:
    def __init__(self, template, browser):
        self.template = template
        self.browser = browser

    def run(self):
        followedCount = 0
        for accountName in self.template['screen_names']:
            #Check if followers have been cached
            followersCache = Utils.cache(accountName + '_scraped')
            if(followersCache != '1'):
                #Retrieve followers
                followers = {}
                self.browser.get('https://twitter.com/' + accountName + '/followers')
                
                #Grab all followers
                while True:
                    #Wait for page load and get links
                    WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/section/div[1]/div[1]")))
                    followerLinks = self.browser.find_elements_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/section/div[1]/div[1]/div')

                    for followerLink in followerLinks:
                        try:
                            #Init db connection
                            DB.execute('''INSERT OR IGNORE INTO 
                                followers(user_name, user_link, followed, followed_at, parent_account) VALUES(?, ?, ?, ?, ?);''', (
                                    followerLink.find_element_by_css_selector('a').get_attribute('href').replace('https://twitter.com/', ''),
                                    followerLink.find_element_by_css_selector('a').get_attribute('href'),
                                    True if ('Following' in followerLink.text or 'Pending' in followerLink.text) else False,
                                    '', accountName,
                                )
                            )
                        except:
                            print('Ignoring...') #Some load without data
                    
                    #Handle infinite scroll (https://dev.to/mr_h/python-selenium-infinite-scrolling-3o12)
                    last_height = self.browser.execute_script("return document.body.scrollHeight") # Get scroll height
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #Scroll to bottom
                    time.sleep(5) # Wait to load page

                    # Calculate new scroll height and compare with last scroll height
                    new_height = self.browser.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        # If heights are the same it will exit the function
                        break
                    last_height = new_height

                Utils.cache(accountName + '_scraped', 1, 43200)

            #Get updated list from db
            followers = DB.selectAll("SELECT * FROM followers WHERE parent_account = ? and followed = 0 limit ?;", (accountName, self.template['amount']))
        
            #Loop through followers and follow
            for follower in followers:
                
                #Load user page
                print("Following " + follower['user_name'])
                self.browser.get(follower['user_link'])
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="@' + follower['user_name'] + '"]')))
                
                #Follow user
                try:
                    followBtn = self.browser.find_element_by_xpath('//span[text()="Follow"]')
                    followBtn.click()
                except:
                    print('User already followed')

                #Update user as followed
                DB.execute('''UPDATE followers SET 
                    followed = ?,
                    followed_at = ? 
                    WHERE id = ?;''', (1, str(datetime.now()), follower['id'])
                )

                followedCount += 1

                print("Taking a short rest...")
                time.sleep(randrange(self.template['sleep_delay'] * 0.6, self.template['sleep_delay']))

        #Final output
        print("Followed " + str(followedCount) + " people")

        