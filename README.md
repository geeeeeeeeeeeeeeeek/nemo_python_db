# Nemo-Python-Db
```
简易的数据操作库，用来便捷的操作数据库
```
## 使用步骤
1. 安装此库： pip install -i https://test.pypi.org/simple/ nemo-python-db
2. 创建数据库类，继承NemoBaseDb。
3. 实现_target_table()方法，返回指定需要操作的目标表。
4. 实现_exec_sql(sql, conditions),调用真正执行SQL的方法，传入参数为sql+参数。
5. 初始化__init__()方法中，指定需要操作的数据表列。
6. 在项目其他引入定义好的数据库类，使用即可。

## 数据库操作一些方法介绍(NemoBaseDb)：  
```
insert(), 按定义的字段全量新增(包含None列)。  
insert_selective(), 按对象中具体有值的列选择性新增。  
update(conditions, conditions), 按定义的字段全量更新(包含None列)，传入更新条件。  
update_selective_(conditions), 按对象中具体有值的列选择性更新，传入更新条件。  
delete(conditions), 按条件删除数据。 
find_dict_by(conditions), 传入查询条件，按条件查询，返回dict类型的列表。
count_by(conditions), 传入查询条件，按条件查询，返回符合条件的总数。
``` 
## 通用查询条件汇总(NemoQueryCondition):
```
start_build()， 开始构建查询条件对象，返回此查询对象。
limit(start_index, page_size)，设置分页条件, limit start_index, page_size，返回此查询对象。
order_by(order_by_str)， 添加排序条件, order by order_by_str，返回此查询对象。
order_by_asc(columns), 添加排序字段，order by columns asc，返回此查询对象。
order_by_desc(columns)， 添加排序字段，order by columns desc，返回此查询对象。
group_by(group_by_str)， 设置分组条件, group by group_by_str，返回此查询对象。

and_equals(column, value), 添加条件and colunm=value, 返回此查询对象。
and_not_equals(column, value)， 添加条件and colunm!=value, 返回此查询对象。
and_like(column, value)， 添加条件and colunm like value, 返回此查询对象。
and_great_then(column, value)， 添加条件and colunm>value, 返回此查询对象。
and_great_equals_then(column, value)， 添加条件and colunm>=value, 返回此查询对象。
and_less_then(column, value)， 添加条件and colunm<value, 返回此查询对象。
and_less_equals_then(column, value)， 添加条件and colunm<=value, 返回此查询对象。
and_between(column, start_value, end_value)， 添加条件and colunm between start_value and end_value, 返回此查询对象。
and_in(column, value_list)， 添加条件and colunm in (value), 返回此查询对象。
and_not_in(column, value_list)， 添加条件and colunm not in (value), 返回此查询对象。
and_is_null(column)， 添加条件and colunm is null, 返回此查询对象。
and_is_not_null(column)， 添加条件and colunm is not null, 返回此查询对象。
and_quota(input_condition)， 添加子条件and (...), 返回此查询对象。

or_equals(column, value), 添加条件or colunm=value, 返回此查询对象。
or_not_equals(column, value)， 添加条件or colunm!=value, 返回此查询对象。
or_like(column, value)， 添加条件or colunm like value, 返回此查询对象。
or_great_then(column, value)， 添加条件or colunm>value, 返回此查询对象。
or_great_equals_then(column, value)， 添加条件or colunm>=value, 返回此查询对象。
or_less_then(column, value)， 添加条件or colunm<value, 返回此查询对象。
or_less_equals_then(column, value)， 添加条件or colunm<=value, 返回此查询对象。
or_between(column, start_value, end_value)， 添加条件or colunm between start_value or end_value, 返回此查询对象。
or_in(column, value_list)， 添加条件or colunm in (value), 返回此查询对象。
or_not_in(column, value_list)， 添加条件or colunm not in (value), 返回此查询对象。
or_is_null(column)， 添加条件or colunm is null, 返回此查询对象。
or_is_not_null(column)， 添加条件or colunm is not null, 返回此查询对象。
or_quota(input_condition)， 添加子条件or (...), 返回此查询对象。

```

## Demo/Example:
```
# coding:utf8
"""
@author Nemo
@time 2021/12/03 11:50
"""
from nemo_python_db.nemo_base_db import NemoBaseDb
from nemo_python_db.nemo_base_query_conditions import NemoQueryCondition

from utils import conf


class UserDao(NemoBaseDb):
    """
    测试数据库操作类，继承自NemoBaseDb
    """

    def __init__(self):
        self.id = None
        self.name = None
        self.password = None

    @staticmethod
    def _target_table():
        """
        指定操作目标表
        """
        return "sys_user"

    def _exec_sql(self, sql, conditions):
        """
        自定义执行SQL方法
        :sql 解析得到的SQL，参数使用%s占位
        :conditions list类型的参数列表
        """
        conf.execute_data_sql_statement(sql, conditions)


if __name__ == '__main__':
    user = UserDao()
    user.name = 'nemo'
    user.password = '123456'
    # insert into sys_user(name, password) values(%s, %s)
    user.insert_selective()

    conditions = NemoQueryCondition.start_build()\
        .and_equals('name', 'nemo')\
        .and_equals('password', '123456')
    # select id, name, password from sys_user where name=%s and password=%s
    rows = UserDao.find_dict_by(conditions)
    if rows:
        for row in rows:
            print(row)

```
 

