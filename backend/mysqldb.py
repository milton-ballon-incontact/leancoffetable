import pymysql
import time
import datetime
import sys
import json

class DBMySQL:
    def __init__(self, ip, usr, pwd, db):
        self.ip = ip
        self.usr = usr
        self.pwd = pwd
        self.datbase = db


    def conn(self):
        try:
            self.db = pymysql.connect(self.ip,self.usr,self.pwd,self.datbase)
            self.cursor = self.db.cursor()
            return 0
        except pymysql.err.OperationalError as err:
            if err.args[0] == '2003':
                return 1 # Unable to connect
            if err.args[0] == '1045':
                return 2 # Fault user ow password
            return 4 # Unknown error

    def disconn(self):
        self.db.close()


    def db_set(self, sql):
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
        except:
            # Rollback in case there is any error
            print("Exception error: {0}".format(sys.exc_info()[0]))
            self.db.rollback()


    def db_get(self, sql):
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            # Rollback in case there is any error
            print("Exception error: {0}".format(sys.exc_info()[0]))


    def test_connection(self):
        res = self.conn()
        if not res == 0:
            return res
        sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'DBName'"
        restup = ()
        restup = self.db_get(sql)
        if not len(restup):
            return 3 # No database


##############################################################


    def get_users(self):
        userlist = []
        sql = "SELECT * FROM user"
        usertup = self.db_get(sql)
        for user in usertup:
            userlist.append({'user': user[0]})
        return userlist


    def get_user(self, user):
        uservalues = []
        usertup = ()
        sql = "SELECT * FROM user WHERE user = '%s'" % user
        usertup = self.db_get(sql)
        if len(usertup):
            usertup = usertup[0]
            uservalues.append({'user': usertup[0], 'name': usertup[1], 'password': usertup[2],'mail': usertup[3]})
        return uservalues


    def check_user(self, user):
        if self.get_user(user):
            return True
        else:
            return False


    def add_user(self, obj):
        # obj expected dictionary {user: 'user', name: 'name', password: 'password}
        sql = \
              "INSERT INTO user(user,name,password,mail,created,updated) \
VALUES ('%s','%s','%s','%s',null,null) ON DUPLICATE KEY UPDATE \
name='%s',password='%s',mail='%s',created=null,updated=null" % \
(obj['user'],obj['name'],obj['password'],obj['mail'],obj['name'],obj['password'],obj['mail'])
        self.db_set(sql)


    def del_user(self, user):
        sql = "DELETE FROM user WHERE user='%s'" % user
        self.db_set(sql)


###############################################################


    def get_boards(self):
        boardlist = []
        boardtup = ()
        sql = "SELECT * FROM board"
        boardtup = self.db_get(sql)
        for board in boardtup:
            boardlist.append({'boardid': board[0]})
        return boardlist


    def add_board(self, obj):
        # obj expected dictionary {username: 'username', boardname: 'boardname', startdate: 'startdate'}
        sql = \
              "INSERT INTO board(user,name,startdate,votenum,created,updated) \
VALUES ('%s','%s','%s','%s',null,null) ON DUPLICATE KEY UPDATE \
user='%s',name='%s',startdate='%s',votenum='%s',created=null,updated=null" % \
(obj['username'], obj['boardname'], obj['startdate'],obj['votenum'],obj['username'], \
 obj['boardname'],obj['startdate'],obj['votenum'])
        print(sql)
        self.db_set(sql)

    def update_board(self, obj):
        # obj expected dictionary {boardid: 'boardid', user: 'user', name: 'name', date:'date'}
        sql = \
            "INSERT INTO board(boardid,user,name,startdate,votenum,created,updated) \
VALUES ('%s','%s','%s','%s','%s',null,null) ON DUPLICATE KEY UPDATE \
user='%s',name='%s',startdate='%s',votenum='%s',created=null,updated=null" % \
(obj['boardid'],obj['username'], obj['boardname'], obj['startdate'],obj['votenum'], \
 obj['username'], obj['boardname'],obj['startdate'],obj['votenum'])
        self.db_set(sql)


    def get_board(self, boardid):
        boardvalues = []
        sql = "SELECT * FROM board WHERE boardid = '%s'" % boardid
        boardtup = self.db_get(sql)
        if len(boardtup):
            boardtup = boardtup[0]
            boardvalues.append({'boardid': boardtup[0], 'name': boardtup[1], 'user': boardtup[2], 'date':boardtup[3],'votenum':boardtup[4]})
        return boardvalues


    def check_board(self, boardid):
        if self.get_board(boardid):
            return True
        else:
            return False


    def del_board(self, boardid):
        sql = "DELETE FROM board WHERE boardid = '%s'" % boardid
        self.db_set(sql)


################################################################


    def get_topics(self, boardid):
        topiclist = []
        sql = "SELECT * FROM topic WHERE boardid = '%s'" % boardid
        topictup = self.db_get(sql)
        for topic in topictup:
            topiclist.append({'topicid': topic[0]})
        return topiclist


    def add_topic(self, obj):
        sql = \
            "INSERT INTO topic(boardid,heading,description,user,created,updated) \
VALUES ('%s','%s','%s','%s',null,null) ON DUPLICATE KEY UPDATE \
boardid='%s',heading='%s',description='%s',user='%s',created=null,updated=null" % \
            (obj['boardid'], obj['heading'], obj['description'], obj['username'], \
             obj['boardid'], obj['heading'], obj['description'], obj['username'])
        self.db_set(sql)


    def update_topic(self, obj):
        sql = \
            "INSERT INTO topic(boardid,heading,description,user,created,updated) \
VALUES ('%s','%s','%s','%s',null,null) ON DUPLICATE KEY UPDATE \
boardid='%s',heading='%s',description='%s',user='%s',created=null,updated=null" % \
            (obj['boardid'], obj['heading'], obj['description'], obj['username'], \
             obj['boardid'], obj['heading'], obj['description'], obj['username'])
        self.db_set(sql)


    def get_topic(self, topicid):
        topicvalues = []
        sql = "SELECT * FROM topic WHERE topicid = '%s'" % topicid
        topictup = self.db_get(sql)
        if len(topictup):
            topictup = topictup[0]
            topicvalues.append({'topicid':topictup[0],'boardid':topictup[1],'heading': topictup[2],
                                'description': topictup[3], 'user':topictup[4]})
        return topicvalues


    def check_topic(self, topicid):
        if self.get_topic(topicid):
            return True
        else:
            return False


    def del_topic(self, topicid):
        sql = "DELETE FROM topic WHERE topicid = '%s'" % topicid
        self.db_set(sql)


###################################################################


    def get_votes(self,boardid,topicid):
        votelist = []
        sql = "SELECT * FROM votes WHERE topicid = '%s'" % topicid
        votetup = self.db_get(sql)
        for vote in votetup:
            votelist.append({'voteid': vote[0]})
        return votelist


    def add_vote(self, obj):
        sql = \
            "INSERT INTO votes(user,topicid) \
VALUES ('%s','%s') ON DUPLICATE KEY UPDATE user='%s',topicid='%s'" % \
        (obj['user'], obj['topicid'],obj['user'], obj['topicid'])
        self.db_set(sql)


    def get_vote(self, topicid, voteid):
        votevalues = []
        sql = "SELECT * FROM votes WHERE voteid = '%s'" % voteid
        votetup = self.db_get(sql)
        if len(votetup):
            votetup = votetup[0]
            votevalues.append({'user': votetup[1],'topicid': votetup[2]})
        return votevalues


    def check_vote(self, voteid):
        if self.get_vote(voteid):
            return True
        else:
            return False


    def del_vote(self, voteid):
        sql = "DELETE FROM votes WHERE voteid = '%s'" % voteid
        self.db_set(sql)
