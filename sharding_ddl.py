#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import sys
import argparse

reload(sys)
sys.setdefaultencoding('utf8')


class ShardingDDL(object):
    """为给出的DDL语句生成多个DDL SQL 语句分片"""

    def __init__(self):
        self.files = []

    def avg_split(self, sharding_count=0, database_count=0):
        """ 平局分片
        通过总共的分片数和需要存放在多少个数据库中进行平均的分片
        Args:
            sharding_count: 总共需要分片的数据量
            database_count: 存放分片数的数据库个数
        Return
            start: 一个数据库中分片开始的下标号
            end: 一个数据库中分片结束的下标号
        Raise: None

        Example:
            sharding_count = 512
            database_count = 4
            return [
                (0, 128),
                (128, 256),
                (256, 384),
                (384, 512),
            ]
        """

        db_shard_count = int(math.ceil(float(sharding_count) / database_count)) # 获得每个库读分片数

        # 计算需要循环的次数

        # 生成每个库中sharing表的 start 和 end 值
        start_end_value = []
        start = 0 # 每个分片的 start
        end = 0 # 每个分片的 end
        for count in range(database_count):

            start = end
            end += db_shard_count

            if end > sharding_count: # 如果最后一个库的标号大于分片数,角标为分片数.
                end = sharding_count

            if start >= end: # 如果开始标号大于等于结束标号直接退出
                break

            start_end_value.append((start, end))

        return start_end_value

    def gen_ddl(self, sql='', start=0, end=0):
        """通过给与的开始分片号和结束分片号生成相关语句
        Args:
            start: 开始分片号
            end: 结束分片号
        Return: sqls
            [
                '''CREATE TABLE t_1;''',
                '''CREATE TABLE t_2;''',
                '''CREATE TABLE t_3;''',
                '''CREATE TABLE t_4;''',
            ]
        Raise: None
        """

        sqls = []
        for i in range(start, end):
            sqls.append(sql.format(num = i))

        return sqls


    def append_sql2file(self, sql='', filename=''):
        """将传入的SQL语句使用append的方式添加到指定的文件
        Args:
            sql: 传入的SQL语句
            filename: 追加的文件名
        Return: None
        Raise: None
        """

        with open(filename, 'a') as f:
            f.write(sql)

    def mysql_shell(self, filename='{filename}', host='{host}',
			              port='{port}', db_name='{db_name}'):
        """打印出执行创建表命令
        Args:
            filename: 文件名
        Return: None
        Raise: None
        """
        shell = 'mysql -uken -pguoguofei@dba123 -h{host} -P{port} -D{dbname} < {filename}'.format(
                host = host,
                port = port,
                dbname = db_name,
                filename=filename,)

        return shell

    def print_clean_file_shell(self):
        """ 清理生成的SQL文件
        通过给定的文件名, 生成rm -f file 命令
        """
        for filename in self.files:
            print 'rm -f {filename}'.format(filename=filename)

def parse_args():
    """解析命令行传入参数"""
    usage = """
Description:
    The script load a file data to mysql table
    """
    # 创建解析对象并传入描述
    parser = argparse.ArgumentParser(description = usage)
    # 添加 一共有多少分片 参数
    parser.add_argument('--sharding_count', dest='sharding_count', required = True,
                      action='store', default='512',
                      help='一共有多少个分片', metavar='512')
    # 添加 有多少个数据库可以分配 参数
    parser.add_argument('--database-count', dest='database_count',
                      action='store', default=4, required = True,
                      help='你需要将多个分片平均分配到多少个数据库中', metavar='4')
    # 添加 文件名 参数
    parser.add_argument('--filename', dest='filename', required = True,
                      action='store', default='sharding_db',
					  help='指定文件的命不需要指定后缀',
					  metavar='sharding_db')
    # 添加 需要在哪个数据库中执行 参数
    parser.add_argument('--database', dest='db_name', required = False,
                      action='store', default='db_name',
                      help='指定SQL语句需要在哪个库中执行', metavar='db_name')

    args = parser.parse_args()

    return args

def main():

    args = parse_args() # 解析传入参数

    # 初始化传入参数
    filename = args.filename
    sharding_count = int(args.sharding_count)
    database_count = int(args.database_count)
    db_name = args.db_name


    ddl_sql = '''
CREATE TABLE `hongbao_city_map_{num}` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `hongbao_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '红包id',
  `city_id` int(11) NOT NULL DEFAULT 0 COMMENT '城市id',
  `is_valid` tinyint(4) NOT NULL DEFAULT 1 COMMENT '1(有效) 0(无效)',
  `is_deleted` tinyint(4) NOT NULL DEFAULT 1 COMMENT '1(删除) 0(未删除)',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '更新时间',
  `drc_check_time` TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '仅供DRC数据校验使用',
  PRIMARY KEY (`id`),
  KEY `ix_hongbao_id` (`hongbao_id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_drc_check_time` (`drc_check_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='红包与城市关联表';
    '''

    sharding_ddl = ShardingDDL()

    # 获得每个库的分片氛围
    sharding_range = sharding_ddl.avg_split(sharding_count = sharding_count,
                                            database_count = database_count)

    for start, end in sharding_range:
        ddl_sqls = sharding_ddl.gen_ddl(sql = ddl_sql,
                                        start = start,
                                        end = end)

        gen_filename = '{name}_{start}_{end}.sql'.format(
            name = filename,
            start = start,
            end = end,
        )

        sharding_ddl.files.append(gen_filename)

        for sql in ddl_sqls:
            sharding_ddl.append_sql2file(sql = sql,
                                         filename = gen_filename)
        print sharding_ddl.mysql_shell(filename = gen_filename,
				                       db_name = db_name)


    sharding_ddl.print_clean_file_shell()



if __name__ == '__main__':
    main()
