from src.Action import Action
import json
class Agent:
    def __init__(self,db,oauth):
        self.data_base = db
        self.action = Action(db)
        self.oauth = oauth
        self.TWEET_URL = "https://api.twitter.com/2/tweets"
        self.RETWEET_URL = "https://api.twitter.com/2/users/-/retweets"
        self.LIKE_URL = "https://api.twitter.com/2/users/-/likes"
        self.FOLLOW_URL = "https://api.twitter.com/2/users/-/following"
        self.MUTE_URL = "https://api.twitter.com/2/users/-/muting"
    def create_agent(self,agent_id,username):
        self.data_base.execute(
            "INSERT INTO AGENTS (agent_id, username) VALUES (?, ?)",
            (agent_id, username)
        )
        self.data_base.commit()
    def is_exist(self,agent_id):
        return  bool(self.data_base.execute(
            "SELECT * FROM AGENTS WHERE agent_id = ?", (agent_id,)
        ).fetchone())
    def is_verified(self,username):
        return self.data_base.execute(
            "SELECT * FROM AGENTS WHERE username = ?", (username,)
        ).fetchone()[2]
    def get_unverifed(self):
        return self.data_base.execute(
            "SELECT agent_id,username FROM AGENTS WHERE status = 'unverified' "
        ).fetchall()
    def get_verifed(self):
        return self.data_base.execute(
            "SELECT agent_id,username,status FROM AGENTS WHERE status != 'unverified' "
        ).fetchall()
    def update(self,agent_id,action):
        if action == "verify" or action =='unban':
            self.data_base.execute(
                "UPDATE AGENTS SET status = 'verified' WHERE agent_id = ?;",(agent_id,)
            )
        elif action =='reject':
            self.data_base.execute(
                "UPDATE AGENTS SET status = 'rejected' WHERE agent_id = ?;",(agent_id,)
            )
        elif action =='ban':
            self.data_base.execute(
                "UPDATE AGENTS SET status = 'banned' WHERE agent_id = ?;",(agent_id,)
            )
        self.data_base.commit()
    def tweet(self,text):      
        result = json.loads(self.oauth.post(self.TWEET_URL, json={"text": text}).text)
        
        try :
            if result["data"]["text"]:
                
                return {"status":200}
            else:
                return {"status":400}
        except:
            return {"status":505}
    def retweet(self,user_id,tweet_id):
        result = json.loads(self.oauth.post(self.RETWEET_URL.replace("-",user_id), json={"tweet_id": tweet_id}).text)
        try :
            if result["data"]["retweeted"]:
                self.action.addtoLog('Retweet',user_id,tweet_id)
                return {"status":200}
            else:
                return {"status":400}
        except:
            return {"status":505}
    def like(self,user_id,tweet_id):
        result = json.loads(self.oauth.post(self.LIKE_URL.replace("-",user_id), json={"tweet_id": tweet_id}).text)
        try :
            if result["data"]["liked"]:
                self.action.addtoLog('Like',user_id,tweet_id)
                return {"status":200}
            else:
                return {"status":400}
        except:
            return {"status":505}
    def reply(self,user_id,text,tweet_id):
        result = json.loads(self.oauth.post(self.TWEET_URL, json={"text": text,"reply": {"in_reply_to_tweet_id": tweet_id }}).text)
        try :
            if result["data"]["text"]:
                self.action.addtoLog('Comment',user_id,tweet_id)
                return {"status":200}
            else:
                return {"status":400}
        except:
            return {"status":505}
    def follow(self,user_id,target_id):
        result = json.loads(self.oauth.post(self.FOLLOW_URL.replace("-",user_id), json={"target_user_id": target_id}).text)
        try :
            if result["data"]["following"] or result["data"]["pending_follow"]:
                self.action.addtoLog('Follow',user_id)
                return {"status":200}
            else:
                return {"status":400}
        except:
            return {"status":505}
    def mute(self,user_id,target_id):
        result = json.loads(self.oauth.post(self.MUTE_URL.replace("-",user_id), json={"target_user_id": target_id}).text)
        try :
            if result["data"]["following"] or result["data"]["pending_follow"]:
                self.action.addtoLog('Mute',user_id)
                return {"status":200}
            else:
                return {"status":400}
        except:
            return {"status":505}
    def get_score(self,user_id):
        return int(self.data_base.execute(
            "SELECT score FROM AGENTS WHERE agent_id = (?) ",(user_id,)
        ).fetchone()[0][0])
    
        
