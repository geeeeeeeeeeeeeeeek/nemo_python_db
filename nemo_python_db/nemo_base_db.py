# coding:utf8
"""
@author Nemo
@time 2021/08/22 21:12
"""
import abc

from typing import Iterable
from .nemo_base_query_conditions import NemoQueryCondition


class NemoBaseDb:
    """
    通用基础数据库操作类
    """

    __metaclass__ = abc.ABCMeta

    def insert(self):
        """
        全量数据新增
        """
        data_info = self.__dict__
        # 全部列
        keys = data_info.keys()
        # 取得所有值，按key顺序转为列表
        data_list = [data_info.get(column) for column in keys]
        return self._insert(keys, data_list)

    def insert_selective(self):
        """
        选择性新增，只操作有值的列
        """
        # 选择性新增的列和数据
        selective_keys, selective_data = self._get_selective()
        return self._insert(selective_keys, selective_data)

    def _insert(self, keys, data_list):
        """
        数据新增
        """
        # 需新增的列
        _columns = ",".join(keys)
        # 新增值得占位符
        value_keys = ",".join(["%s" for _ in keys])
        sql = """INSERT INTO {table} ({keys}) VALUES ({value_keys})""".format(
            table=self._target_table(),
            keys=_columns,
            value_keys=value_keys
        )
        return self._exec_sql(sql, data_list)

    def update(self, conditions=NemoQueryCondition.start_build()):
        """
        全量更新
        """
        data_info = self.__dict__
        keys = [_key for _key in data_info.keys()]
        data = [data_info.get(_key) for _key in keys]
        return self._update(keys, data, conditions)

    def update_selective(self, conditions=NemoQueryCondition.start_build()):
        """
        选择性更新
        """
        selective_keys, selective_data = self._get_selective()
        return self._update(selective_keys, selective_data, conditions)

    def _update(self, columns, data_list, conditions=NemoQueryCondition.start_build()):
        """
        更新
        """
        columns = "=%s, ".join([_column for _column in columns]) + "=%s"
        where_conditions, where_list = self._get_condition_sql(conditions)
        sql = """
                    UPDATE {table} SET {columns}
                    {where_conditions}
                """.format(
            table=self._target_table(),
            columns=columns,
            where_conditions=where_conditions
        )
        for where_item in where_list:
            data_list.append(where_item)
        return self._exec_sql(sql, data_list)

    @classmethod
    def delete(cls, conditions=NemoQueryCondition.start_build()):
        """
        按条件删除
        """
        self = cls()
        where_conditions, where_list = self._get_condition_sql(conditions)
        sql = """
            DELETE FROM {table} {where_conditions}
        """.format(
            table=self._target_table(),
            where_conditions=where_conditions
        )
        return self._exec_sql(sql, where_list)

    @classmethod
    def find_dict_by(cls, conditions=NemoQueryCondition.start_build()):
        """
        按条件查询，返回dict类型的列表
        """
        self = cls()
        # 查询条件sql，查询条件数据
        where_conditions, where_list = self._get_condition_sql(conditions)

        # 排序字段
        order_by = ''
        # 分页信息
        limit = ''
        # 分组字段
        group_by = ''
        if isinstance(conditions, NemoQueryCondition):
            if conditions.order_by_list:
                order_by_condition = ",".join([order_by_item for order_by_item in conditions.order_by_list])
                order_by = "ORDER BY %s" % format(order_by_condition)
                # where_list.append(order_by_condition)
            if conditions.group_by_str:
                group_by = "GROUP BY %s"
                where_list.append(conditions.group_by_str)
            if conditions.page_size is not None and conditions.start_index is not None:
                limit = "LIMIT {start_index},{page_size}".format(
                    start_index=conditions.start_index,
                    page_size=conditions.page_size
                )

        sql = """
            SELECT 
            {columns} 
            FROM {table}
            {conditions}
            {group_by}
            {order_by}
            {limit}
        """.format(
            columns=self._select_columns(),
            table=self._target_table(),
            conditions=where_conditions,
            order_by=order_by,
            group_by=group_by,
            limit=limit
        )
        result = self._exec_sql(sql, where_list)
        if not result:
            return []
        return result

    @classmethod
    def count_by(cls, conditions=NemoQueryCondition.start_build()):
        """
        查询总数
        """
        self = cls()
        where_conditions, where_list = self._get_condition_sql(conditions)
        sql = """
            SELECT count(1) AS cnt FROM {table}
            {conditions}
        """.format(
            table=self._target_table(),
            conditions=where_conditions
        )
        res = self._exec_sql(sql, where_list)
        if not res:
            return 0
        return dict(res[0]).get('cnt')

    @staticmethod
    def _get_condition_sql(conditions=NemoQueryCondition.start_build()):
        """
        获取查询条件语句
        """
        where_conditions = ""
        where_list = []
        if conditions:
            if isinstance(conditions, NemoQueryCondition):
                # 查询对象，调用解析方法即可
                return conditions.parse()
            if isinstance(conditions, Iterable):
                conditions = dict(conditions)
            else:
                conditions = conditions.__dict__
            count = 0
            for key in conditions:
                val = conditions.get(key)
                if val:
                    if count == 0:
                        where_conditions += 'WHERE '
                        count += 1
                    else:
                        where_conditions += ' AND '
                    where_conditions += ' %s = %s ' % (key, '%s')
                    where_list.append(val)
        return where_conditions, where_list

    def _select_columns(self):
        """
        拼装需要查询的列名
        """
        data_info = self.__dict__
        keys = data_info.keys()
        return ",".join(keys)

    def _get_selective(self):
        """
        获取选择性更新、新增的列和数据
        """
        data_info = self.__dict__
        keys = data_info.keys()
        # 需要新增的列
        selective_keys = []
        # 需要新增的数据
        selective_data = []
        for _key in keys:
            data = data_info.get(_key)
            if data:
                selective_keys.append(_key)
                selective_data.append(data)
        return selective_keys, selective_data

    @staticmethod
    @abc.abstractmethod
    def _target_table():
        """
        目标表表名，需要操作的表
        """
        pass

    @abc.abstractmethod
    def _exec_sql(self, sql, conditions):
        """
        执行一个sql
        :sql sql
        :conditions 参数列表
        """
        pass
