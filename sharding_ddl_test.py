#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import unittest
import sys
from sharding_ddl import ShardingDDL

reload(sys)
sys.setdefaultencoding('utf8')


class ShardingDDLTest(unittest.TestCase):
    """ 单元测试(ShardingDDL)
    为给出的DDL语句生成多个DDL SQL 语句分片
    """

    def test_avg_split_512_4(self):
        """测试平局分片的方法"""

        sharding_ddl = ShardingDDL()
        cus_results = [
            (0, 128),
            (128, 256),
            (256, 384),
            (384, 512),
        ]
        results = sharding_ddl.avg_split(sharding_count = 512,
                                         database_count = 4)
        print cus_results
        print results

        self.assertEquals(cus_results, results)

    def test_avg_split_511_4(self):
        """测试平局分片的方法"""

        sharding_ddl = ShardingDDL()
        cus_results = [
            (0, 128),
            (128, 256),
            (256, 384),
            (384, 511),
        ]
        results = sharding_ddl.avg_split(sharding_count = 511,
                                         database_count = 4)
        print cus_results
        print results

        self.assertEquals(cus_results, results)

    def test_avg_split_508_4(self):
        """测试平局分片的方法"""

        sharding_ddl = ShardingDDL()
        cus_results = [
            (0, 127),
            (127, 127*2),
            (127*2, 127*3),
            (127*3, 127*4),
        ]
        results = sharding_ddl.avg_split(sharding_count = 508,
                                         database_count = 4)
        print cus_results
        print results

        self.assertEquals(cus_results, results)

    def test_avg_split_3_4(self):
        """测试平局分片的方法"""

        sharding_ddl = ShardingDDL()
        cus_results = [
            (0, 1),
            (1, 2),
            (2, 3),
        ]
        results = sharding_ddl.avg_split(sharding_count = 3,
                                         database_count = 4)
        print cus_results
        print results

        self.assertEquals(cus_results, results)

    def test_gen_ddl(self):

        sql = '''
        CREATE TABLE `hongbao_city_map_{num}`;
        CREATE TABLE `hongbao_brand_map_{num}`;
        CREATE TABLE `hongbao_restaurant_map_{num}`;
        '''

        cus_results = [
        '''
        CREATE TABLE `hongbao_city_map_0`;
        CREATE TABLE `hongbao_brand_map_0`;
        CREATE TABLE `hongbao_restaurant_map_0`;
        ''',
        '''
        CREATE TABLE `hongbao_city_map_1`;
        CREATE TABLE `hongbao_brand_map_1`;
        CREATE TABLE `hongbao_restaurant_map_1`;
        ''',
        '''
        CREATE TABLE `hongbao_city_map_2`;
        CREATE TABLE `hongbao_brand_map_2`;
        CREATE TABLE `hongbao_restaurant_map_2`;
        ''',
        ]

        sharding_ddl = ShardingDDL()
        results = sharding_ddl.gen_ddl(sql, 0, 3)

        print cus_results
        print results

        self.assertEquals(cus_results, results)

if __name__ == '__main__':
    unittest.main()
