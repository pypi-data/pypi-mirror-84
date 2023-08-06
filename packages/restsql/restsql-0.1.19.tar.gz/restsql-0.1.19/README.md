## RestSQL介绍

[点此查看](https://git.code.oa.com/tencent_cloud_mobile_tools/Athena/blob/develop/doc/interface/rest-sql-protocol/rest-sql-protocol.md)


## 示例
```

```python
from schema import Schema, BoolField, NumberField, StringField
from restsql import RestSqlAgent
from restsqldb import EnumDataBase
from middleware import RestSqlMiddleware


class User(Schema):
    table_name = 'user'
    fields = {
        'id': NumberField(),
        'version': NumberField(),
        'login': StringField(),
        'email': StringField(),
        'password': StringField(),
        'is_disabled': BoolField(),
        'company': StringField()
    }

class TestMiddlerware(RestSqlMiddleware):
    @staticmethod
    def process_query(query):
        # 自定义处理过程
        if 'select' not in query:
            raise RuntimeError('Missing select field in query')


db_settings = [
        {
            'name': 'sqlite_test',
            'type': EnumDataBase.SQLITE,
            'host': 'grafana.db',
            'user': '',
            'schema': [User]
        }
    ]

restsql = RestSqlAgent(db_settings=db_settings, middlewares=[TestMiddlerware])

test_query = {
        'select': {
            'from': 'user',
            'fields': ['version', 'login', 'email', 'password', 'company'],
            'filter': {'version__gte': 0, 'company': 'ff'},
            'aggregation': [],
            'group_by': []
        },
        'join': [],
        'sort': [],
        'fields': [],
        'limit': 200
    }

results = restsql.query(test_query)

```

## 概念介绍

### db_settings

数据库配置定义，包含`name`,`db_name`,`type`,`port`,`host`,`user`,`password`, `schema`等八个字段

### Schema

用于定义表结构，必须继承与`Schema`，必须定义两个类属性：`table_name`,`fields`。代表表名和可开放查询字段，字段暂时只支持`Number`, `String`, `Boolean`三种类型

### middleware

查询前对query的处理模块，例如格式检查，也可以对query做自定义修改。暂时只支持自定义的形式，后续会默认添加基本的格式检查

## 发布

1. 打包: `python setup.py sdist build`。
2. 上传: 
    * 安装twine工具: `pip install twine`
    * 发布: `twine upload dist/*`


## Todo List

* 完善日志
* 完善异常类型与异常检测，目前只有`RuntimeError`一种异常类型
* 定义默认middleware
* 兼容py2py3