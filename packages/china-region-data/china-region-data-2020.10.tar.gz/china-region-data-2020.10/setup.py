# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['china_region_data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'china-region-data',
    'version': '2020.10',
    'description': '中国行政区域数据',
    'long_description': '# 中国行政区域数据\n\n根据[中华人民共和国民政部](http://www.mca.gov.cn/article/sj/xzqh/)中的数据处理而成。\n\n由于时间跨度过长（从 1980 年至今），故而部分地区的名称或行政级别已经发生改变，本仓库的存储原则为“编码唯一，以新换旧”。即同一个行政编码，认定为同一个地区，地区名称以民政部门最新公开的行政区域划分数据中的名称为准。且，为保持向前兼容，一些过去存在但后来去除的行政区域编码，本仓库仍然保留，以方便一些古旧的数据能正常使用。\n\n## 安装\n\n```bash\npip install china-region-data\n```\n\n## 样例\n\n```python\nfrom china_region_data import Region\n\n\n广东 = Region("广东省")\n深圳 = Region("广东省深圳市")\n南山 = Region("广东省深圳市南山区")\nassert 广东.name == "广东省"\nassert 广东.level == 1\n\nfor 广东城市 in 广东.subordinate:\n    assert 广东城市.level == 2\n\nassert 深圳.superior == 广东\nassert 南山.superior.superior == 广东\nassert 南山 in 南山.superior\nassert 南山 in 南山.superior.superior\n\n北京 = Region("110000")\nassert 北京.name == 北京.fullname == "北京市"\nassert 北京 not in 广东\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/china-region-data',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
