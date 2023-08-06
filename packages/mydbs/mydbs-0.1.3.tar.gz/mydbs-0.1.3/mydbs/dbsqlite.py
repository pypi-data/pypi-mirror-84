from mydbs import *
from sqlite3 import connect


class Sqlite(BaseDB):
    def __init__(self, db):
        super(Sqlite, self).__init__()

        self.__db = db
        self.set_conn(connect(self.__db))

        self.set_cursor((self.get_conn().cursor()))

    def show_tables(self):
        """
        列出数据库中所有现存表
        :return: 由表名字符串组成的列表
        """
        sql = 'SELECT name FROM sqlite_master;'
        return [tb_name[0] for tb_name in self.get_cursor().execute(sql).fetchall()]

    def create_table(self, table_name='', pri_key_name='', **item_type_dict):
        """
        Sqlite创建表
        :param table_name:数据表名称
        :param pri_key_name: 数据表主键名称
        :param item_type_dict: 关键字与数据类型键值对字典
        :return: 0为执行成功
        """
        sql_sqlite = 'CREATE TABLE IF NOT EXISTS %s (%s);'
        item_type_str = ''
        for k, v in item_type_dict.items():
            if k != pri_key_name:
                item_type_str += k + ' ' + v + ' NOT NULL,'
            else:
                item_type_str += k + ' ' + v + ' PRIMARY KEY AUTOINCREMENT NOT NULL, '
        item_type_str = item_type_str.strip(',')
        return self.get_cursor().execute(sql_sqlite % (table_name, item_type_str))

    def desc_table(self, table_name=''):
        """
        列出表的结构(Sqlite给出创建表的sql语句)
        :param table_name: 表名称
        :return: 表的结构表
        """
        sql = 'SELECT SQL FROM sqlite_master WHERE NAME = "%s";'
        return self.get_cursor().execute(sql % table_name).fetchall()[0][0]

    def alter(self):
        pass

    def pri_key_reset(self, table_name='', pri_key_name=''):
        pass
