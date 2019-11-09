from db import SqlDB
import re


class Precondition:
    def __init__(self):
        self.db = SqlDB()

    def write_dict_to_db(self, txt_path):
        self.db.creat_cur()
        sql = "insert into dict_database (word,exp) values(%s,%s)"
        fd = open(txt_path, "r")
        for line in fd:
            res = re.findall(r'(\S+)\s+(.*)', line)[0]
            print(res)
            self.db.execute(sql, res)
        self.db.commit()
        self.db.close()
        fd.close()

if __name__ == '__main__':
    pre = Precondition()
    pre.write_dict_to_db("dict.txt")
