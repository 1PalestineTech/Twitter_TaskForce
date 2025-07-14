
CREATE TABLE AGENTS (
    agent_id TEXT,
    username TEXT UNIQUE,
    status TEXT DEFAULT 'unverified',
    score INTEGER DEFAULT 0,
    PRIMARY KEY (agent_id)
);

CREATE TABLE ADMINS(
    username TEXT,
    password TEXT
);

CREATE TABLE PROFILES(
    profile_id TEXT,
    username TEXT UNIQUE,
    PRIMARY KEY (profile_id)
);
CREATE TABLE TASKS(
    task_id INTEGER,
    name TEXT UNIQUE,
    score INTEGER,
    PRIMARY KEY (task_id)
);
CREATE TABLE POSTS(
    post_id TEXT,
    profile_id TEXT,
    post_body  TEXT,
    status TEXT DEFAULT 'unverified',
    date date NUMERIC DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_id),
    FOREIGN KEY (profile_id) REFERENCES PROFILES(profile_id)
);
CREATE TABLE ACTIONS(
    profile_id TEXT,
    task_id INTEGER,
    FOREIGN KEY (profile_id) REFERENCES PROFILES(profile_id),
    FOREIGN KEY (task_id) REFERENCES TASKS(task_id)
);
CREATE TABLE LOG(
    task_id INTEGER,
    post_id TEXT DEFAULT 'profile/action',
    agent_id TEXT,
    FOREIGN KEY (task_id) REFERENCES TASKS(task_id),
    FOREIGN KEY (agent_id) REFERENCES TAGENTS(agent_id),
    FOREIGN KEY (post_id) REFERENCES POSTS(post_id)
);
INSERT INTO TASKS(name,score) VALUES('Comment',10);
INSERT INTO TASKS(name,score) VALUES('Retweet',15);
INSERT INTO TASKS(name,score) VALUES('Like',5);
INSERT INTO TASKS(name,score) VALUES('Follow',10);
INSERT INTO TASKS(name,score) VALUES('Mute',10);
INSERT INTO TASKS(name,score) VALUES('Tweet',20);