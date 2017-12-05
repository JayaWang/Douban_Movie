# -*- coding: utf-8 -*-

import MySQLdb

class GetProxy:
    def __init__(self):
        host = '127.0.0.1'
        user = 'root'
        password = '228228'
        db_name = 'Tencent'
        try:
            self.db_conn = MySQLdb.connect(host, user, password, db_name, charset = "utf8") #连接数据库
        except Exception as e:
            print ('数据库连接错误' + str(e))

    def Query_MySQL(self, sql_command):
        try:
            db_cur = self.db_conn.cursor()
            db_cur.execute(sql_command)
            data = db_cur.fetchall()
            return data
        except Exception as e:
            print ('读取执行' + sql_command + '失败' + str(e))

    def GetIP(self): #API
        sql = "SELECT ip, port FROM proxys WHERE id >= ((SELECT MAX(id) FROM proxys)-(SELECT MIN(id) FROM proxys)) * RAND() + (SELECT MIN(id) FROM proxys)  LIMIT 1"
        try:
            ip_middle = self.Query_MySQL(sql)
            ip = str(ip_middle[0][0]) + ':' + str(ip_middle[0][1])

            '''ip_ok = {"http": "http://" + ip,
                     "https": "http://" + ip,}'''

            ip_ok = "http://" + ip
            return ip_ok
        except Exception as e:
            print ('读取代理ip错误' + str(e))