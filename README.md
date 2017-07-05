# sharding_ddl
批量生成多个分片的DDL语句

### 使用方法
##### 查看帮助
```
hh@docker55:~/python$ python sharding_ddl.py --help
usage: sharding_ddl.py [-h] --sharding_count 512 --database-count 4 --filename
                       sharding_db [--database db_name]

Description: The script load a file data to mysql table

optional arguments:
  -h, --help            show this help message and exit
  --sharding_count 512  一共有多少个分片
  --database-count 4    你需要将多个分片平均分配到多少个数据
                        库中
  --filename sharding_db
                        指定文件的命不需要指定后缀
  --database db_name    指定SQL语句需要在哪个库中执行
```
##### 执行
```
hh@docker55:~/python$ python sharding_ddl.py --sharding_count 126 --database-count 4 --filename test_sharding --database test
mysql -uroot -p127.0.0.1 -h{host} -P{port} -Dtest < test_sharding_0_32.sql
mysql -uroot -p127.0.0.1 -h{host} -P{port} -Dtest < test_sharding_32_64.sql
mysql -uroot -p127.0.0.1 -h{host} -P{port} -Dtest < test_sharding_64_96.sql
mysql -uroot -p127.0.0.1 -h{host} -P{port} -Dtest < test_sharding_96_126.sql
rm -f test_sharding_0_32.sql
rm -f test_sharding_32_64.sql
rm -f test_sharding_64_96.sql
rm -f test_sharding_96_126.sql
```
##### 查看结果
```
hh@docker55:~/python$ ll
total 36
drwxrwxr-x 2 hh hh 4096 Jul  5 16:16 ./
drwxr-xr-x 9 hh hh 4096 Jul  5 16:10 ../
-rw-r--r-- 1 hh hh 6008 Jul  5 16:10 sharding_ddl.py
-rw-r--r-- 1 hh hh 3105 Jul  4 21:28 sharding_ddl_test.py
-rw-rw-r-- 1 hh hh  886 Jul  5 16:16 test_sharding_0_32.sql
-rw-rw-r-- 1 hh hh  896 Jul  5 16:16 test_sharding_32_64.sql
-rw-rw-r-- 1 hh hh  896 Jul  5 16:16 test_sharding_64_96.sql
-rw-rw-r-- 1 hh hh  866 Jul  5 16:16 test_sharding_96_126.sql

hh@docker55:~/python$ head test_sharding_0_32.sql 

    CREATE TABLE t_0;
    
    CREATE TABLE t_1;
    
    CREATE TABLE t_2;
    
    CREATE TABLE t_3;
    
    CREATE TABLE t_4;

hh@docker55:~/python$ tail test_sharding_96_126.sql 
    CREATE TABLE t_121;
    
    CREATE TABLE t_122;
    
    CREATE TABLE t_123;
    
    CREATE TABLE t_124;
    
    CREATE TABLE t_125;
```
