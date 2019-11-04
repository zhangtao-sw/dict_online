import pymysql


class SqlDB:
    def __init__(self, host="localhost", port=3306, user="root", password='123456', database="dict", charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.creat_db()

    def creat_db(self):
        self.db=pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,database=self.database,charset=self.charset)

    def creat_cur(self):
        self.cur=self.db.cursor()

    def insert(self,sql,list_):
        try:
            self.cur.execute(sql, list_)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
    def exit_(self):
        self.cur.close()
        self.db.close()


