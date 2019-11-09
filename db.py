import pymysql
import hashlib


class SqlDB:
    def __init__(self, host="localhost", port=3306, user="root", password='123456', database="dict", charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.creat_db()
        self.salt = "*#06#"

    def encryption(self,passwd):
        # 对密码进行加密处理
        hash = hashlib.md5(self.salt.encode())
        hash.update(passwd.encode())
        return hash.hexdigest()

    def creat_db(self):
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                  database=self.database, charset=self.charset)

    def creat_cur(self):
        self.cur = self.db.cursor()

    def insert(self, sql, list_):
        try:
            self.cur.execute(sql, list_)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
    def execute(self, sql, list_):
        self.cur.execute(sql,list_)

    def commit(self):
        try:
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def close(self):
        self.db.close()

    def exit_(self):
        self.cur.close()

    def register(self, name, password):
        sql = "select * from user where name='%s';" % name
        self.cur.execute(sql)
        resule = self.cur.fetchone()
        if resule:
            return False
        password = self.encryption(password)
        sql = "insert into user (name,password) values(%s,%s);"
        try:
            self.cur.execute(sql, [name, password])
            self.db.commit()
            return True
        except Exception as e:
            print (e)
            self.db.rollback()
            return False

    def login(self, name, password):
        sql = "select * from user where name='%s';" % name
        self.cur.execute(sql)
        resule = self.cur.fetchone()
        if not resule:
            return False
        password = self.encryption(password)
        sql = "select * from user where password='%s';" % password
        self.cur.execute(sql)
        resule_2 = self.cur.fetchone()
        if not resule_2:
            return False
        return True

    def query(self,name,word):
        sql = "select * from dict_database where word='%s';" %word
        self.cur.execute(sql)
        resule = self.cur.fetchone()
        print ("res:",resule)
        if not resule:
            return False
        print ("begin insert his")
        sql="insert into history (name,word) values(%s,%s);"
        self.cur.execute(sql,[name,word])
        try:
            self.db.commit()
        except Exception as e:
            print (e)
            self.db.rollback()
            return False
        return resule

    def his(self,name):
        sql="select * from history where name='%s' order by time desc limit 10;"%name
        self.cur.execute(sql)
        res=self.cur.fetchall()
        if not res:
            return False
        return res

