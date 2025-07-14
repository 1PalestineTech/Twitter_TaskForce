class Task:
    def __init__(self,db):
        self.data_base = db

    def get_tasks(self):
        return  self.data_base.execute(
            "SELECT task_id,name FROM TASKS"
        ).fetchall()
    def taskId(self,task_name):
        return  self.data_base.execute(
            "SELECT task_id FROM TASKS WHERE name = (?)",
            (task_name,)
        ).fetchall()[0][0]
    def getTaskScore(self,task_name):
        return  int(self.data_base.execute(
            "SELECT score FROM TASKS WHERE name = (?)",
            (task_name,)
        ).fetchall()[0][0])
