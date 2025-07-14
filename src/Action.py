from src.Task import Task

class Action:
    def __init__(self,db):
        self.data_base = db
        self.task = Task(db)
        
    def assignTasks(self,profile_id,tasks):
        for task in tasks:
            self.data_base.execute("INSERT INTO ACTIONS (profile_id, task_id) VALUES (?, ?)",(profile_id,int(task)))
        self.data_base.commit()
    def editTasks(self,profile_id,tasks):
        self.remove()
        for task in tasks:
            self.data_base.execute("INSERT INTO ACTIONS (profile_id, task_id) VALUES (?, ?)",(profile_id,int(task)))
        self.data_base.commit()
    def remove(self,profile_id):
        self.data_base.execute("DELETE FROM ACTIONS WHERE profile_id = ?",(profile_id,))
        self.data_base.commit()
    def isDone(self,task_id,agent_id,post_id='profile/action',):
        return bool(
            self.data_base.execute("SELECT * FROM LOG WHERE task_id=(?) AND post_id=(?) AND agent_id=(?)",
                                   (task_id,post_id,agent_id)).fetchone()
        )
    def getProfiles(self,task_id):
        rows = self.data_base.execute("SELECT profile_id FROM ACTIONS WHERE task_id=(?)",
                                   (task_id,)).fetchall()
        profile_ids = ",".join([row[0] for row in rows])
        return profile_ids
    def updateScore(self,user_id,taskname):
        curent_score = self.get_score(self,user_id)
        point = self.action.task.getTaskScore(taskname)
        self.data_base.execute(
                "UPDATE AGENTS SET score  = ? WHERE agent_id = ?;",(curent_score+point,user_id)
            )
    
    def addtoLog(self,task_name,agent_id,post_id=""):
        task_id = self.task.taskId(task_name)
        if post_id == "":
            self.data_base.execute(
            "INSERT INTO LOG (agent_id, task_id) VALUES (?, ?)",(agent_id,int(task_id))
        )
        else:
           self.data_base.execute(
            "INSERT INTO LOG (agent_id, task_id,post_id) VALUES (?, ?, ?)",(agent_id,int(task_id),post_id)
        ) 
        self.updateScore(agent_id,task_name)
        self.data_base.commit()
    