from src.Action import Action
from src.Task import Task
from src.Profile import Profile
class Post:
    def __init__(self,db):
        self.data_base = db
        self.action = Action(db) 
        self.task = Task(db)
        self.profile =Profile(db,10)
    def get_posts(self):
        rows = self.data_base.execute("""
        SELECT 
            POSTS.post_id,
            POSTS.post_body,
            POSTS.status,
            POSTS.date,
            PROFILES.username,
            GROUP_CONCAT(TASKS.name, ', ') AS actions
        FROM 
            POSTS
        JOIN PROFILES ON POSTS.profile_id = PROFILES.profile_id
        JOIN ACTIONS ON PROFILES.profile_id = ACTIONS.profile_id
        JOIN TASKS ON ACTIONS.task_id = TASKS.task_id
        GROUP BY POSTS.post_id
        ORDER BY POSTS.date DESC
    """).fetchall()
        posts = []
        for row in rows:
            post_id, post_body, status, _, username, actions = row
            posts.append({"post_id":post_id,"post_body":post_body,"status":status,"username":username,"actions":actions.split(",")})
        return posts
    def update(self,post_id,action):
        if action == "verify" or action =='accept':
            self.data_base.execute(
                "UPDATE POSTS SET status = 'verified' WHERE post_id = ?;",(post_id,)
            )
        elif action =='reject' or  action =='remove':
            self.data_base.execute(
                "UPDATE POSTS  SET status = 'rejected' WHERE agent_id = ?;",(post_id,)
            )
        self.data_base.commit()
    def selectPost(self,profile_ids):
        return self.data_base.execute(
                "SELECT post_id,profile_id FROM POSTS WHERE profile_id IN (?) AND status = 'verified';",(profile_ids,)
            ).fetchall()
    def filterPosts(self,agent_id,task_name):
        task_id = self.task.taskId(task_name)
        profiles_ids = self.action.getProfiles(task_id)
        result = []
        if task_name == 'Mute' or  task_name ==  'Follow':
            for profile_id in profiles_ids.split(","):
                if not self.action.isDone(task_id,agent_id):
                    result.append(profile_id)
            return self.profile.profileData(",".join(result))
        else:
            
            posts_id = self.selectPost(profiles_ids)
            for post_id,profile_id in posts_id :
                if not self.action.isDone(task_id,agent_id,post_id):
                    result.append(self.profile.profileData(profile_id,post_id))
            return result
    def postExist(self,post_id):
        return bool(self.data_base.execute(
                "SELECT * FROM POSTS WHERE post_id = (?)",(post_id,)
            ).fetchone())
    def addPost(self,post_id,profile_id):
        if not self.postExist(post_id):
            self.data_base.execute(
                "INSERT INTO POSTS (post_id, profile_id) VALUES (?, ?)",(post_id,profile_id)
            )
            self.data_base.commit()
        