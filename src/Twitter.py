import json
from src.Post import Post
from time import sleep
class Twitter:
    def __init__(self,db,oauth,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
    
        self.post = Post(db)

        self.oauth = oauth(
                    API_KEY,
                    client_secret = API_SECRET,
                    resource_owner_key = ACCESS_TOKEN,
                    resource_owner_secret =ACCESS_TOKEN_SECRET,
                )
        self.ID_URL = "https://api.twitter.com/2/users/by/username/"
        self.TWEET = "https://api.twitter.com/2/users/-/tweets"
        self.database = db
    def get_id(self,username):
        response = json.loads(self.oauth.get(self.ID_URL+username).text)
        try : 
            return response["data"]["id"]
        except:
            return "something went wrong"
    def get_tweets(self,user_id):
        response = json.loads(self.oauth.get(self.TWEET.replace("-",user_id),json={"max_results": 1}).text)
        
        return response
    def get_profiles(self):
        return self.database.execute("""
        SELECT profile_id FROM PROFILES
        """).fetchall()
    def get_posts(self):
        profiles_id =  self.get_profiles()
        for id in profiles_id:
            try :
                post_id = self.get_tweets(id[0])["data"][0]["id"]
                
                sleep(30)
                self.post.addPost(post_id,id[0])
            except:
                pass