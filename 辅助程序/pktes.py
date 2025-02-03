def is_valid_schedule(course, time_slot, teacher, classroom, schedule):
    # 检查教师和教室的可用性
    if teacher['availability'][time_slot] == 0 or classroom['availability'][time_slot] == 0:
        return False
    # 检查是否与其他课程冲突
    for scheduled_course in schedule:
        if scheduled_course['time_slot'] == time_slot:
            if scheduled_course['teacher'] == teacher or scheduled_course['classroom'] == classroom:
                return False
    return True

def schedule_courses(courses, teachers, classrooms, schedule, index=0):
    if index >= len(courses):
        return True  # 所有课程已安排完毕
    course = courses[index]
    for time_slot in range(len(teachers[0]['availability'])):
        for teacher in teachers:
            for classroom in classrooms:
                if is_valid_schedule(course, time_slot, teacher, classroom, schedule):
                    # 安排课程
                    schedule.append({
                        'course': course,
                        'time_slot': time_slot,
                        'teacher': teacher,
                        'classroom': classroom
                    })
                    # 递归安排下一个课程
                    if schedule_courses(courses, teachers, classrooms, schedule, index + 1):
                        return True
                    # 回溯，取消安排
                    schedule.pop()
    return False

# 示例数据
courses = ['语文', '数学', '英语', '政治', '历史', '物理', '化学', '音乐', '体育', '美术', '信息', '劳技', '社团', '外教', '自习'] * 2  # 每个班级有16门课程，共30个班级
teachers = [{'name': 'Teacher {}'.format(i), 'availability': [1] * 10} for i in range(30)]  # 30名教师，每人10个可用时间段
classrooms = [{'name': 'Room {}'.format(i), 'availability': [1] * 10} for i in range(30)]  # 30个教室，每个教室10个可用时间段
schedule = []

if schedule_courses(courses, teachers, classrooms, schedule):
    print("Course schedule successfully created:")
    for entry in schedule:
        print(entry)
else:
    print("Failed to create a valid course schedule.")