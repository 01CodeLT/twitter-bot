import time
from src.db import DB
from src.utils import Utils
from random import randrange
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UnfollowFollowing:
    def __init__(self, template, browser):
        self.template = template
        self.browser = browser

    def run(self):
        unfollowedCount = 0

        #Get recently followed
        recentlyFollowed = DB.selectAll("select * from `followers` where date(`followed_at`) < date('now', '-5 days') and `followed_back` is NULL;", ())
        
        #Check if followers have followed back
        for followedUser in recentlyFollowed:
            self.browser.get(followedUser['user_link'])

            #Get following back status
            try:
                WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Following' or text()='Pending']")))
                followsBack = self.browser.find_elements_by_xpath('//span[text()="Follows you"]')
                if(len(followsBack) > 0):
                    DB.execute('''UPDATE followers SET 
                        followed_back = ?
                        WHERE id = ?;''', (1, followedUser['id'])
                    )
                else:
                    #Click unfollow
                    self.browser.find_element_by_xpath('//span[text()="Following" or text()="Pending"]').click()
                    
                    #Click confirm
                    WebDriverWait(self.browser, 7).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Discard' or text()='Unfollow']")))
                    self.browser.find_element_by_xpath('//span[text()="Discard" or text()="Unfollow"]').click()
                    
                    #Mark as not followed back
                    DB.execute('''UPDATE followers SET 
                        followed_back = ?
                        WHERE id = ?;''', (0, followedUser['id'])
                    )
                    unfollowedCount = unfollowedCount + 1
                    print('Stopped following ' + followedUser['user_name'])
            except Exception as e:
                print(e)
                #Mark as unfollowed
                # DB.execute('''UPDATE followers SET 
                #     followed_back = 0
                #     WHERE id = ?;''', (followedUser['id'])
                # )
                print('Error occured checking follow status of ' + followedUser['user_name'])
                
            print("Taking a short rest...")
            time.sleep(randrange(self.template['sleep_delay'] * 0.6, self.template['sleep_delay']))

        #Final output
        print("Unfollowed " + str(unfollowedCount) + " people")