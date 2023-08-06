#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
desc:数据库操作类
@note:
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件匹配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
'''

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

import Config

'''
Config是一些数据库的配置文件
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
    获取连接对象：conn = Mysql.getConn()
    释放连接对象;conn.close()或del conn
'''

class Mysql(object):
    #连接池对象
    __pool = None

#数据库构造函数，从连接池中取出连接，并生成操作游标
    def __init__(self):
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()

#@summary: 静态方法，从连接池中取出连接
#@return MySQLdb.connection
    def __getConn(self):

        if Mysql.__pool is None:
            __pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=20 ,
                              host=Config.DBHOST , port=Config.DBPORT , user=Config.DBUSER , passwd=Config.DBPWD ,
                              db=Config.DBNAME,use_unicode=False,charset=Config.DBCHAR,cursorclass=DictCursor)
        return __pool.connection()

    def __query(self,sql,param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        return count

    '''
    @summary: 执行查询，并取出num条结果
    @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    @param num:取得的结果条数
    @param param: 可选参数，条件列表值（元组/列表）
    @return: result list/boolean 查询到的结果集
    '''

    def getAll(self,sql,param=None):
        count = self.__query(sql,param)
        if count>0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self,sql,param=None):
        count = self.__query(sql,param)
        if count>0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self,sql,num,param=None):
        count = self.__query(sql,param)
        if count>0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    '''
    @summary: 向数据表插入一条记录
    @param sql:要插入的ＳＱＬ格式
    @param value:要插入的记录数据tuple/list
    @return: insertId 受影响的行数
    '''
    def insertOne(self,sql,value):
        self._cursor.execute(sql,value)
        return self.__getInsertId()


    '''
    @summary: 向数据表插入多条记录
    @param sql:要插入的ＳＱＬ格式
    @param values:要插入的记录数据tuple(tuple)/list[list]
    @return: count 受影响的行数
    '''
    def insertMany(self,sql,values):
        count = self._cursor.executemany(sql,values)
        return count

    #获取当前连接最后一次插入操作生成的id,如果没有则为０"""
    def __getInsertId(self):
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def update(self,sql,param=None):
        return self.__query(sql,param)

    def delete(self,sql,param=None):
        return self.__query(sql,param)

    #@summary: 开启事务
    def begin(self):
        self._conn.autocommit(0)

    #@summary: 结束事务
    def end(self,option='commit'):
        if option=='commit':
            self._conn.commit()
        else:
            self._conn.rollback()


    #@summary: 释放连接池资源
    def dispose(self,isEnd=1):
        if isEnd==1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()


