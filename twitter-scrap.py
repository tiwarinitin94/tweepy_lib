import tweepy
import csv
from datetime import datetime
import time


# Create API object

# API KEY  - ######
# API SECRET KEY - ############################
# Access Token - ############################
# Access token Key - ############################################


def create_api():
    consumer_key = "#######"
    consumer_secret = "########"
    access_token = "#########################"
    access_token_secret = "######################"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("API created")
        return api
    except Exception as e:
        print("Error creating API")
        raise e


def getUserDetails(api, username):
    user = api.get_user(username)

    data = api.user_timeline(screen_name=username, count=20, include_rts=False, tweet_mode='extended')

    user_det = {
        "user": user,
        "name": user.screen_name,
        "username": username,
        "followers": user.followers_count,
        "following": user.friends_count,
        "profile_pic": user.profile_background_image_url,
        "bio": user.description,
        "recent_tweets": data,
        "total_tweets": user.statuses_count

    }

    return user_det


def main():
    file1 = open('twitter_remaining.txt', 'r')
    Lines = file1.readlines()

    count = 0

    fieldsProfile = [
        'dataExtract',
        'Statusretweet',
        'Listedcount',
        'Favoritescount',
        'Followerscount',
        'Username',
        'Description',
        'Followingcount',
        'Tweetscount',
        'Statuscreatedat',
        'Name'
    ]

    fieldsTweets = [
        'Username'
        'Name',
        'Tweetsource',
        'Likes',
        'Retweets',
        'postID',
        'Twittername',
        'Tweet',
        'Userdescription',
        'Location',
        'Userfollowers',
        'dataExtract',
        'Datetime'
    ]

    # print(len(Lines))
    with open('twitter_profile_data.csv', 'a', encoding="utf-8") as csvfile:

        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldsProfile)
        csvwriter.writeheader()
        # writing the fields

    with open('twitter_tweet_data.csv', 'a', encoding="utf-8") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldsTweets)
        csvwriter.writeheader()

        for l in Lines:

            l = l.strip('\n')
            print(l)
            api = create_api()
            det = getUserDetails(api, l.strip(' '))

            with open('twitter_profile_data.csv', 'a', encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
                # writing the fields

                fields = [
                    'dataExtract',
                    det['total_tweets'],
                    det['user'].listed_count,
                    det['user'].favourites_count,
                    det['followers'],
                    det['username'],
                    det['bio'],
                    det['following'],
                    det['total_tweets'],
                    'Statuscreatedat',
                    det['user'].name,
                ]
                csvwriter.writerow(fields)

            with open('twitter_tweet_data.csv', 'a', encoding="utf-8") as fd:
                for tweet in det['recent_tweets']:
                    csvwriter = csv.writer(fd)

                    created_at = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    fields = [
                        l,
                        tweet.user.name,
                        tweet.source,
                        tweet.favorite_count,
                        tweet.retweet_count,
                        created_at ,
                        None,
                        tweet.full_text,
                        None,
                        det['user'].location,
                        det['followers'],
                        'dataExtract',

                    ]

                    csvwriter.writerow(fields)

    # api = create_api()
    # det = getUserDetails(api, "njtiwari")
    # print(det.favourites_count)


if __name__ == "__main__":
    main()

#
# user = api.get_user("FlaviaArrudaDF")
#
# stuff = api.user_timeline(screen_name = 'FlaviaArrudaDF', count = 1, include_rts = True)


# 3 - tweets last week
# 4 - retweets last week
# 5 - likes last week
# 8 - most used hashtags
# 9 - last tweets (img/video + text)
# 10 - likes on each tweet
# 11 - retweets on each tweet
# 12 - data of creation of each tweet
# 13 - bio


# Create a tweet
# api.update_status("Hello Tweepy")
