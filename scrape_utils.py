from tqdm import tqdm
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date, timedelta

def scrape_twitter(query=None, user=None, since=str(date.today()-timedelta(days=1)), until=str(date.today()+timedelta(days=1))):
    """
    Scrape tweets from Twitter.
    query - search for tweets containing this string
    user - search for tweets by this user
    since - search for tweets since this date
    until - search for tweets until this date (non-inclusive)

    data saved in csv file
    """

    if all(v is None for v in {query, user}):
        raise ValueError("Must specify either query or user")

    search_str = f"{query} " if query else ""
    search_str += f"from:{user} " if user else ""
    search_str += f"since:{since} " if since else ""
    search_str += f"until:{until} " if until else ""
    print(search_str)
    
    tweets_df = pd.DataFrame(columns=["tweet_id", "date", "user_name", "tweet", "retweets", "likes", "quote_tweets", "replies", "retweeted_tweet", "quoted_tweet"])
    tweets_df.to_csv(f"tweets_{query if query else user}.csv", index=False)

    for tweet in tqdm(sntwitter.TwitterSearchScraper(search_str).get_items()):
        tweet_elem = {"tweet_id": tweet.id,
                      "date":tweet.date,
                      "user_name": tweet.user.username,
                      "tweet":tweet.content,
                      "retweets": tweet.retweetCount,
                      "likes": tweet.likeCount,
                      "quote_tweets":tweet.quoteCount,
                      "replies":tweet.replyCount,
                      "retweeted_tweet":tweet.retweetedTweet,
                      "quoted_tweet":tweet.quotedTweet,
                      }
        # append tweet to dataframe of tweets
        tweet_df = tweets_df.append(tweet_elem, ignore_index = True)
        # continously append new data to the csv
        tweet_df.to_csv(f"tweets_{query if query else user}.csv", mode="a", index=False, header=False)
    
    return

def scrape_twitter_users(users, filename=""):
    """
    Scrape tweets from Twitter.
    users - list of users to scrape
    """

    tweets_user_df = pd.DataFrame(columns=["user_id", "user_name", "display_name", "description", "verified", "created", "followers", "following", "tweets", "location"])
    tweets_user_df.to_csv(f"tweets_{filename}_users.csv", index=False)

    for user in tqdm(users):
        for tweet in sntwitter.TwitterSearchScraper(f"from:{user}").get_items():
            user_elem = {
                "user_id": tweet.user.id,
                "user_name": tweet.user.username,
                "display_name": tweet.user.displayname,
                "description": tweet.user.description,
                "verified": tweet.user.verified,
                "created": tweet.user.created,
                "followers": tweet.user.followersCount,
                "following": tweet.user.friendsCount,
                "tweets": tweet.user.statusesCount,
                "location": tweet.user.location,
            }
            break
        user_df = tweets_user_df.append(user_elem, ignore_index = True)
        # write to csv
        user_df.to_csv(f"tweets_{filename}_users.csv", mode="a", index=False, header=False)