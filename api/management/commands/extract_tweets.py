import tweepy
import psycopg2
from django.core.management.base import BaseCommand

# Twitter API v2 credentials
API_KEY = 'm3PL51dtk1vS3OV8tWmzAoK4v'
API_SECRET = 'Ra80HSTUDReiRV9KYiAq7Xd6fxyY8YJ9LJSnyanBALB4Ni3pUY'
ACCESS_TOKEN = '946544777809612801-A5zCTLKXIH3AHeRqX94zufCsAVEnRBU'
ACCESS_TOKEN_SECRET = 'uIz5ffGZR6cG8BTaVzEo2g1VSUMrsqTKajl6gP1c18nWg'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAP2YwQEAAAAAoARqPjJFgJJ5w567vJH3hx5daJk%3DeLDIHFHDAcmNbHuOP9ImqI2h1EscfUcqbuVTJcSQydJa0OYoQo'

# Database credentials
DB_NAME = 'watch_villavo'
DB_USER = 'django'
DB_PASSWORD = 'django'
DB_HOST = 'localhost'

class Command(BaseCommand):
    help = 'Extract tweets related to robberies in Villavicencio and store them in the database'

    def handle(self, *args, **kwargs):
        # Connect to Twitter API
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
            cur = conn.cursor()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error connecting to the database: {e}'))
            return

        query = 'robo OR asalto OR hurto lang:es -is:retweet place:"Villavicencio"'
        
        try:
            # Fetch tweets
            tweets = client.search_recent_tweets(query=query, tweet_fields=['created_at', 'geo', 'text'], max_results=100)
            # Process and store tweets
            for tweet in tweets.data:
                if tweet.geo:
                    cur.execute("""
                        INSERT INTO tweets (tweet_text, created_at, latitude, longitude)
                        VALUES (%s, %s, %s, %s)
                    """, (tweet.text, tweet.created_at, tweet.geo['coordinates'][0], tweet.geo['coordinates'][1]))
            
            conn.commit()
            self.stdout.write(self.style.SUCCESS('Tweets extracted and stored in the database!'))

        except tweepy.TweepyException as e:
            self.stdout.write(self.style.ERROR(f'Twitter API error: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
        finally:
            # Ensure database connection is closed
            if cur:
                cur.close()
            if conn:
                conn.close()