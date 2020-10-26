# Twitter bot
This is a python bot which uses selenium to follow and unfollow users on twitter. Currently you can only set it to follow users who are following a particular account.

To get started clone the project, then download chromedriver from https://chromedriver.chromium.org/ and place the exe named as "chromedriver.exe" in the root folder of the project. Also, add your settings in a "settings.json" file in the root folder of the project...
*Example...*

    {
        "username": "TWITTER_USERNAME",
        "password": "TWITTER_PASSWORD",
        "templates": [{
            "name": "Follow users",
            "type": "follow_user_followers",
            "screen_names": ["TWITTER_USERNAME"], //Grab a list of followers from these acccounts and follow them
            "sleep_delay": 20,
            "amount": 20
        }, {
            "name": "Unfollow users",
            "type": "unfollow_following", //Unfollow users who haven't followed back after a while
            "sleep_delay": 20
        }]
    }

Run "py index.py" in your terminal to run the script.

**DISCLAIMER!** The use of this bot is at your own risk. I do not encourage the use of twitter bots and I am not responsible if Twitter decides to take action against you. Please read the twitter terms and conditions before using this project.