text='''{
  "basic": {
    "days": "5",
    "cycle": "每周",
    "max_duration": "45",
    "break_interval": "10",
    "daily_periods": "9",
    "class_count": "6",
    "grade": "三"
  },
  "time_rules": [
    [
      "周一",
      "有",
      "08:00",
      "17:00",
      "6"
    ],
    [
      "周二",
      "有",
      "08:00",
      "17:00",
      "6"
    ],
    [
      "周三",
      "有",
      "08:00",
      "17:00",
      "6"
    ],
    [
      "周四",
      "有",
      "08:00",
      "17:00",
      "6"
    ],
    [
      "周五",
      "有",
      "08:00",
      "17:00",
      "6"
    ],
    [
      "周六",
      "无",
      "",
      "",
      ""
    ],
    [
      "周日",
      "按需",
      "",
      "",
      "None"
    ]
  ],
  "subjects": [
    {
      "name": "语文",
      "teachers": 3
    },
    {
      "name": "数学",
      "teachers": 2
    },
    {
      "name": "英语",
      "teachers": 2
    },
    {
      "name": "物理",
      "teachers": 2
    },
    {
      "name": "化学",
      "teachers": 3
    },
    {
      "name": "地理",
      "teachers": 4
    },
    {
      "name": "生物",
      "teachers": 1
    },
    {
      "name": "体育",
      "teachers": 3
    },
    {
      "name": "美术",
      "teachers": 2
    },
    {
      "name": "音乐",
      "teachers": 1
    },
    {
      "name": "信息",
      "teachers": 1
    },
    {
      "name": "劳技",
      "teachers": 1
    },
    {
      "name": "综合",
      "teachers": 2
    },
    {
      "name": "道法",
      "teachers": 2
    }
  ]
}'''
def MakeNewJson():
    try:
        open("settings.json")
    except:
        with open("settings.json",'w',encoding='utf8') as f:
            f.write(text)