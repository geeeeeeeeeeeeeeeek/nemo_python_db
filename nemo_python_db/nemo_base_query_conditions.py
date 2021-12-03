# coding:utf8
"""
@author Nemo
@time 2021/08/23 01:42
"""


class _QueryConst:
    """
    一些查询相关常量定义
    """

    def __init__(self):
        pass

    # 连接符
    collection_or = "OR"
    collection_and = "AND"
    collection_and_quota = "AND (%s)"
    collection_or_quota = "OR (%s)"

    # 标识符
    quota_equals = "="
    quota_not_equals = "!="
    quota_like = "LIKE"
    quota_great_then = ">"
    quota_great_equals_then = ">="
    quota_less_then = "<"
    quota_less_equals_then = "<="
    quota_between = "BETWEEN"
    quota_in = "IN"
    quota_not_in = "NOT IN"
    quota_is_null = "IS NULL"
    quota_is_not_null = "IS NOT NULL"


class NemoQueryCondition:
    """
    查询条件组装对象
    """

    def __init__(self):
        # 条件列表
        self.condition_list = []
        # 条件定义： and id = %s
        # 连接符
        self.collection = None
        # 标识符
        self.quota = None
        # 列名
        self.column = None
        # 对应值
        self.c_value = None
        # 分页条件
        self.page_size = None
        self.start_index = None
        # 分组条件
        self.group_by_str = None
        # 排序条件
        self.order_by_list = []

    @staticmethod
    def start_build():
        """
        开始构建参数对象
        """
        return NemoQueryCondition()

    def limit(self, start_index, page_size):
        """
        分页设置
        """
        self.start_index = start_index
        self.page_size = page_size
        return self

    def order_by(self, order_by_str):
        """
        排序设置
        """
        self.order_by_list.append(order_by_str)
        return self

    def order_by_asc(self, columns):
        """
        设置升序
        """
        self.order_by_list.append('%s ASC' % columns)
        return self

    def order_by_desc(self, columns):
        """
        设置降序
        """
        self.order_by_list.append('%s DESC' % columns)
        return self

    def group_by(self, group_by_str):
        """
        分组查询设置
        """
        self.group_by_str = group_by_str
        return self

    @staticmethod
    def _build(collection, quota, column, value):
        """
        构建一个组装对象
        """
        self = NemoQueryCondition()
        self.collection = collection
        self.quota = quota
        self.column = column
        self.c_value = value
        return self

    def and_equals(self, column, value):
        """
        添加等于条件
        and name=%s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_equals,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def and_not_equals(self, column, value):
        """
        添加不等于条件
        and name!=%s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_not_equals,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def and_like(self, column, value):
        """
        添加like条件
        and name like %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_like,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def and_great_then(self, column, value):
        """
        添加大于条件
        and id > %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_great_then,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def and_great_equals_then(self, column, value):
        """
        添加大于等于条件
        and id >= %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_great_equals_then,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def and_less_then(self, column, value):
        """
        添加小于条件
        and id < %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_less_then,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def and_less_equals_then(self, column, value):
        """
        添加小于等于条件
        and id <= %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_less_equals_then,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def and_between(self, column, start_value, end_value):
        """
        添加区间条件
        and id between %s and %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_between,
            column,
            [start_value, end_value]
        )
        self.condition_list.append(_condition)
        return self

    def and_in(self, column, value_list):
        """
        添加in条件
        and id in (%s)
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_in,
            column,
            value_list
        )
        self.condition_list.append(_condition)
        return self

    def and_not_in(self, column, value_list):
        """
        添加not in 条件
        and id not in (%s)
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_not_in,
            column,
            value_list
        )
        self.condition_list.append(_condition)
        return self

    def and_is_null(self, column):
        """
        添加空判定条件
        and id is null
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_is_null,
            column,
            None
        )
        self.condition_list.append(_condition)
        return self

    def and_is_not_null(self, column):
        """
        添加费控判定条件
        and id is not null
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and,
            _QueryConst.quota_is_not_null,
            column,
            None
        )
        self.condition_list.append(_condition)
        return self

    def and_quota(self, input_condition):
        """
        添加子条件
        and ( id = %s and name = %s )
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_and_quota,
            None,
            None,
            None
        )
        _condition.condition_list.append(input_condition)
        self.condition_list.append(_condition)
        return self

    def or_equals(self, column, value):
        """
        or name=%s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_equals,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def or_like(self, column, value):
        """
        or name like %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_like,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def or_great_then(self, column, value):
        """
        or name > %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_great_then,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def or_great_equals_then(self, column, value):
        """
        or name >= %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_great_equals_then,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def or_less_then(self, column, value):
        """
        or name < %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_less_then,
            column,
            value
        )
        self.condition_list.append(_condition)

    def or_less_equals_then(self, column, value):
        """
        or name <= %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_less_equals_then,
            column,
            value
        )
        self.condition_list.append(_condition)
        return self

    def or_between(self, column, start_value, end_value):
        """
        or name between %s and %s
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_between,
            column,
            [start_value, end_value]
        )
        self.condition_list.append(_condition)
        return self

    def or_in(self, column, value_list):
        """
        or name in (%s)
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_in,
            column,
            value_list
        )
        self.condition_list.append(_condition)
        return self

    def or_not_in(self, column, value_list):
        """
        or name not in (%s)
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_not_in,
            column,
            value_list
        )
        self.condition_list.append(_condition)
        return self

    def or_is_null(self, column):
        """
        or name is null
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_is_null,
            column,
            None
        )
        self.condition_list.append(_condition)
        return self

    def or_is_not_null(self, column):
        """
        or name is not null
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or,
            _QueryConst.quota_is_not_null,
            column,
            None
        )
        self.condition_list.append(_condition)
        return self

    def or_quota(self, input_condition):
        """
        or ( xxx )
        """
        _condition = NemoQueryCondition._build(
            _QueryConst.collection_or_quota,
            None,
            None,
            None
        )
        _condition.condition_list.append(input_condition)
        self.condition_list.append(_condition)
        return self

    def parse(self, first_condition=True):
        """
        解析当前条件
        """
        # 查询条件语句
        where_condition = ""
        # 查询条件数据列表
        where_data_list = []
        # 查询列
        column = self.column
        # 查询标识符
        quota = self.quota
        # 查询连接符
        collection = self.collection
        # 查询值
        value = self.c_value

        # 存在查询列以及对应标识符，则解析当前明细
        if column and quota:
            _where_condition, _where_data_list = self.parse_detail(False, collection, quota, column, value)
            where_condition += _where_condition
            for child_data in _where_data_list:
                where_data_list.append(child_data)

        # 子条件解析
        condition_list = self.condition_list
        for _condition in condition_list:
            _collection = _condition.collection
            _where_condition, _where_data_list = _condition.parse(False)
            # 当前连接符为OR (%s) 或者 AND (%s)，其中第一个子条件需要剔除标识符，避免 AND (AND id=%s)
            if _collection in (_QueryConst.collection_or_quota, _QueryConst.collection_and_quota):
                _where_condition = _where_condition[4:]
                _where_condition = _collection % _where_condition
            where_condition += _where_condition
            [where_data_list.append(child_data) for child_data in _where_data_list]

        # 语句头，需添加WHERE，剔除第一个连接符
        if first_condition and where_condition:
            if where_condition.startswith(_QueryConst.collection_or):
                where_condition = where_condition[2:]
            else:
                where_condition = where_condition[4:]
            where_condition = "WHERE \n           " + where_condition

        return where_condition, where_data_list

    def parse_detail(self, count, collection, quota, column, value):
        """
        解析条件明细
        """
        where_condition = ''
        where_data_list = []
        # and name=%s
        if column:
            if quota in (_QueryConst.quota_in, _QueryConst.quota_not_in):
                # and id in ('%s', '%s')
                split = ",".join(['%s' for _ in value])
                where_condition += " %s %s %s (%s) " % (collection, column, quota, split)
                [where_data_list.append(str(item)) for item in value]
            elif quota == _QueryConst.quota_between:
                # and id between %s and %s
                where_condition += " %s %s %s %s and %s " % (collection, column, quota, '%s', '%s')
                where_data_list.append(value[0])
                where_data_list.append(value[1])
            elif quota in (_QueryConst.quota_is_not_null, _QueryConst.quota_is_null):
                # and id is null
                where_condition += " %s %s %s " % (collection, column, quota)
            else:
                # and id = %s
                where_condition += " %s %s %s %s " % (collection, column, quota, '%s')
                where_data_list.append(value)
        else:
            _condition_list = self.condition_list
            for child_condition in _condition_list:
                child_condition_str, child_data_list = child_condition.parse(count)
                where_condition += child_condition
                for child_data in child_data_list:
                    where_data_list.append(child_data)
        return where_condition, where_data_list
