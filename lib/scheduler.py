import configparser
from collections import defaultdict

WEEKDAY_NAMES = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
WEEKDAY_MAP = {day.lower()[:3]: idx for idx, day in enumerate(WEEKDAY_NAMES)}

def parse_weekdays(weekdays_str):
    """解析星期字符串为星期索引列表"""
    return [WEEKDAY_MAP[day.strip().lower()[:3]] for day in weekdays_str.split(',')]

def generate_timetable(config_path):
    """主函数：输入配置文件路径，返回课表字典"""
    config = configparser.ConfigParser()
    config.read(config_path)

    # 初始化数据结构：班级 -> 星期 -> 节次 -> 科目
    timetable = defaultdict(lambda: defaultdict(dict))
    
    # 解析时间段配置（仅用于验证节次有效性）
    time_slots = {int(k) for k in config['TimeSlots']} if 'TimeSlots' in config else set()

    # 处理所有课程配置
    for section in config.sections():
        if not section.startswith('Course:'):
            continue

        try:
            course = config[section]
            # 解析多班级配置
            classes = [c.strip() for c in course['class'].split(',')]
            # 解析多教师配置（实际未使用，仅为兼容配置）
            teachers = [t.strip() for t in course['teacher'].split(',')]
            
            # 处理班级-教师配对逻辑
            if len(classes) != len(teachers):
                if len(classes) == 1:
                    classes = classes * len(teachers)
                elif len(teachers) == 1:
                    teachers = teachers * len(classes)
                else:
                    raise ValueError("班级与教师数量不匹配")

            subject = course['subject']
            weekdays = parse_weekdays(course['weekdays'])
            start_slot = course.getint('start_slot')
            duration = course.getint('duration', 1)
            slots = range(start_slot, start_slot + duration)

            # 验证时间段有效性
            if not all(s in time_slots for s in slots):
                invalid = [s for s in slots if s not in time_slots]
                raise ValueError(f"无效时间段: {invalid}")

            # 处理每个班级的排课
            for cls in set(classes):  # 去重处理
                for weekday in weekdays:
                    weekday_name = WEEKDAY_NAMES[weekday]
                    for slot in slots:
                        # 冲突检测
                        if slot in timetable[cls][weekday_name]:
                            existing = timetable[cls][weekday_name][slot]
                            raise ValueError(
                                f"冲突：{cls}班 {weekday_name} 第{slot}节 "
                                f"已有【{existing}】，无法安排【{subject}】"
                            )
                        timetable[cls][weekday_name][slot] = subject

        except Exception as e:
            print(f"配置项 {section} 错误: {str(e)}")
            continue

    # 转换为目标格式
    result = {}
    for cls in timetable:
        result[cls] = {}
        for weekday in timetable[cls]:
            # 按节次顺序生成课程列表
            sorted_slots = sorted(timetable[cls][weekday].items())
            result[cls][weekday] = [subject for _, subject in sorted_slots]

    return result

# 使用示例
if __name__ == "__main__":
    config_path = "school.ini"
    timetable = generate_timetable(config_path)
    print(timetable)