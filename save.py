# -*- coding: utf-8 -*-
"""
  Create by leiSong on 2019/8/8 21:55 
  @Email : leisong01@qq.com
  @File : save.py 
  @description: 
"""
import pymysql


class SaveToMysql():
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='******',
            port=3306,  # 数据库端口
            db='******',  # 数据库名
            user='******',  # 数据库用户名
            passwd='******',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def __executeSql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()
        finally:
            pass

    def closeSql(self):
        self.connect.close()
        self.cursor.close()
        print('关闭数据库~~~')

    def openSql(self):
        self.__init__()
        print('打开数据库~~~')

    def __save(self, ip, port, last_time):
        sql = 'insert into proxyip (IP,PORT,last_time) values (%s,%s,%s) ' % ('"'+ip+'"', '"'+port+'"', '"'+last_time+'"')
        self.__executeSql(sql)

    def __update(self, id, ip, port, last_time):
        sql = 'UPDATE proxyip SET IP = %s , PORT= %s, last_time= %s WHERE id = %d' % ('"'+ip+'"', '"'+port+'"', '"'+last_time+'"', id)
        self.__executeSql(sql)

    def __select(self, ip, port):
        sql = 'SELECT ID FROM proxyip WHERE IP=%s AND PORT = %s' % ('"'+ip+'"', '"'+port+'"')
        res = self.cursor.execute(sql)
        self.connect.commit()
        return res

    def __markSuccess(self, id):
        sql = 'UPDATE proxyip SET mark = 100  WHERE id = %d' % id
        self.__executeSql(sql)

    def __markFail(self, id):
        sql = 'UPDATE proxyip SET mark = mark - 1  WHERE id = %d' % id
        self.__executeSql(sql)

    def updateMark(self, id, flag):
        if flag:
            self.__markSuccess(id)
        else:
            self.__markFail(id)

    def getAll(self):
        sql = 'SELECT * FROM proxyip ORDER BY mark DESC, last_time DESC ,id DESC'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def main(self,ip, port, last_time):
        id = self.__select(ip, port)
        if not id:
            self.__save(ip, port, last_time)
        else:
            self.__update(id, ip, port, last_time)
