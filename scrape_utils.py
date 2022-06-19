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
    
    tweets_df = pd.DataFrame(columns=["tweet_id", "date", "tweet", "retweets", "likes", "quote_tweets", "replies", "retweeted_tweet", "quoted_tweet",
                                        "user_name", "user_display_name", "user_description", "user_verified", "user_location", "user_created", "user_followers", "user_following", "user_tweets_count"])
    tweets_df.to_csv(f"tweets_{query if query else user}.csv", index=False)

    for tweet in tqdm(sntwitter.TwitterSearchScraper(search_str).get_items()):
        tweet_elem = {"tweet_id": tweet.id,
                      "date":tweet.date,
                      "tweet":tweet.content,
                      "retweets": tweet.retweetCount,
                      "likes": tweet.likeCount,
                      "quote_tweets":tweet.quoteCount,
                      "replies":tweet.replyCount,
                      "retweeted_tweet":tweet.retweetedTweet,
                      "quoted_tweet":tweet.quotedTweet,
                      "user_name": tweet.user.username,
                      "user_display_name": tweet.user.displayname,
                      "user_description": tweet.user.description,
                      "user_verified": tweet.user.verified,
                      "user_location":tweet.user.location,
                      "user_created":tweet.user.created,
                      "user_followers":tweet.user.followersCount,
                      "user_following":tweet.user.friendsCount,
                      "user_tweets_count":tweet.user.statusesCount,
                      }
        # append tweet to dataframe of tweets
        tweet_df = tweets_df.append(tweet_elem, ignore_index = True)
        # continously append new data to the csv
        tweet_df.to_csv(f"tweets_{query if query else user}.csv", mode="a", index=False, header=False)
    
    return