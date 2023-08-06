# -*- coding: utf-8 -*-

# 生产者
product = "DouYinOne"

# 消费者模块
consume = {
    "DouYinOne": {
        # 执行模式requests/WebDriver
        "run_mode": "requests",
        # 是否需要auth或cookie
        "need_token": False,
        # 是否存储
        "save": False,
    },
    "DouYinTwo": {
        # 执行模式requests/WebDriver
        "run_mode": "requests",
        # 是否需要auth或cookie
        "need_token": False,
        # 是否存储
        "save": False,
    },
    "DouYinThree": {
        # 执行模式requests/WebDriver
        "run_mode": "requests",
        # 是否需要auth或cookie
        "need_token": False,
        # 是否存储
        "save": True,
    },
}

# 存储途径
output = [
    {
        "mongodb":
            {
                "host": "47.116.109.99",
                "port": 27017,
                "user_name": "",
                "password": "",
                "db_name": "competitor_test_data",
            },
    },
    {
        "print": {}
    }
]
