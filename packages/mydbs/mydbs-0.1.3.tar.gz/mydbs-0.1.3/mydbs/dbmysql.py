from mydbs import *
from pymysql import connect


class MySql(BaseDB):
    def __init__(self, user='', pwd='', db='', host='localhost', port=3306, charset='utf8'):
        """
        初始化参数
        :param user: 用户名
        :param pwd: 用户密码
        :param db: 使用的数据库名称
        """
        super(MySql, self).__init__()
        self.__host = host
        self.__user = user
        self.__port = port
        self.__pwd = pwd
        self.__db = db
        self.__charset = charset
        self.set_conn(connect(host=self.__host,
                              user=self.__user,
                              port=self.__port,
                              password=self.__pwd,
                              database=self.__db,
                              charset=self.__charset))

        self.set_cursor(self.get_conn().cursor())

    def show_databases(self):
        """
        列出所有现存数据库
        :return: 数据库名称列表
        """
        sql = 'SHOW DATABASES;'
        self.get_cursor().execute(sql)
        return [ele[0] for ele in self.get_cursor().fetchall()]

    def use_database(self, db_name=''):
        """
        切换数据库
        :param db_name:数据库名称
        :return: 0为执行成功
        """
        sql = 'USE %s;'
        return self.get_cursor().execute(sql % db_name)

    def create_database(self, db_name=''):
        """
        创建新数据库
        :param db_name:数据库名称
        :return: 0为执行成功
        """
        sql = 'CREATE DATABASE %s;'
        return self.get_cursor().execute(sql % db_name)

    def create_table(self, table_name='', pri_key_name='', engine='InnoDB', charset='utf8', **item_type_dict):
        """
        创建新表
        :param table_name: 数据表名称
        :param pri_key_name: 主键名称
        :param engine: 数据库引擎
        :param charset: 数据库字符集
        :param item_type_dict: 关键字与数据类型键值对字典
        :return: 0为执行成功
        """
        item_type_str = ''
        sql = 'CREATE TABLE IF NOT EXISTS %s (%s)ENGINE=%s DEFAULT CHARSET=%s;'
        for k, v in item_type_dict.items():
            if k != pri_key_name:
                item_type_str += k + ' ' + v + ' NOT NULL,'
            else:
                item_type_str += k + ' ' + v + ' PRIMARY KEY AUTO_INCREMENT NOT NULL, '
        item_type_str = item_type_str.strip(',')
        return self.get_cursor().execute(sql % (table_name, item_type_str, engine, charset))

    def alter(self, table_name='', mode='', content=''):
        """
        修改
        :param table_name: 数据表名称
        :param mode: 模式选择
        :param content: 修改内容
        :return: 执行成功返回1
        """
        sql = ''
        if mode == 'drop':
            sql = 'ALTER TABLE %s DROP %s'
        elif mode == 'add':
            sql = 'ALTER TABLE %s ADD %s'
        elif mode == 'modify':
            sql = 'ALTER TABLE %s MODIFY %s'
        elif mode == 'change':
            sql = 'ALTER TABLE %s CHANGE %s'
        self.get_cursor().execute(sql % (table_name, content))
        self.get_conn().commit()
        return 0

    def pri_key_reset(self, table_name='', pri_key_name=''):
        """
        重置数据标主键
        :param table_name: 数据表名称
        :param pri_key_name: 主键名称
        :return: 执行成功返回1
        """
        self.alter(table_name, 'drop', pri_key_name)
        self.alter(table_name, 'add', pri_key_name + ' INT(10) AUTO_INCREMENT PRIMARY KEY FIRST')
        return 0
