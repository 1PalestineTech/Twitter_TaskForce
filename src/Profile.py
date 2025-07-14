from src.Action import Action
from collections import defaultdict
class Profile:
    def __init__(self,db,twitter):
        self.data_base = db 
        self.twitter= twitter
        self.action = Action(db)
    def isExist(self,username):
        return bool(self.data_base.execute(
            "SELECT * FROM PROFILES WHERE username = ?", (username,)
        ).fetchone())
    def remove(self,profile_id):
        self.data_base.execute(
            "DELETE FROM PROFILES WHERE profile_id = ?", (profile_id,)
        )
        self.data_base.commit()
        self.action.remove(profile_id)
    def create(self,username,tasks):
        if not self.isExist(username):
            profile_id = self.twitter.get_id(username)
            self.data_base.execute("INSERT INTO PROFILES (profile_id, username) VALUES (?, ?)",(profile_id,username))
            self.action.assignTasks(profile_id,tasks)
            return True
        return False
    def getProfiles(self):
        rows = self.data_base.execute(
            """SELECT 
    PROFILES.profile_id, 
    PROFILES.username, 
    TASKS.name AS task_name
FROM 
    PROFILES
JOIN 
    ACTIONS ON PROFILES.profile_id = ACTIONS.profile_id
JOIN 
    TASKS ON ACTIONS.task_id = TASKS.task_id;"""
        ).fetchall()
        result = []
        profiles = defaultdict(lambda: {"username": "", "tasks": []})
        for profile_id, username, task_name in rows:
            profiles[profile_id]["username"] = username
            profiles[profile_id]["tasks"].append(task_name)
        for profile_id, data in profiles.items():
            result.append({"id":profile_id,"username":data['username'],"Actions":data['tasks']})
           
        return result
    def profileData(self,profiles_ids,posts_ids=""):
        if posts_ids == "":
            data = self.data_base.execute(
                """
                SELECT profile_id,username
                FROM PROFILES
                WHERE profile_id IN (?)
                """,(profiles_ids,)
            ).fetchall()
        else:
            data = self.data_base.execute(
                """
                SELECT PROFILES.username,PROFILES.profile_id,POSTS.post_id
                FROM PROFILES
                JOIN 
                POSTS ON PROFILES.profile_id = POSTS.profile_id
                WHERE POSTS.profile_id = (?)
                AND POSTS.post_id =(?)
                """,(profiles_ids,posts_ids)
            ).fetchone()
        return data






