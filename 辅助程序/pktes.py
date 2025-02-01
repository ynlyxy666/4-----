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
courses = ['Math', 'Science', 'History']
teachers = [{'name': 'Alice', 'availability': [1, 1, 0, 1]}, {'name': 'Bob', 'availability': [1, 1, 1, 0]}]
classrooms = [{'name': 'Room 101', 'availability': [1, 1, 1, 1]}, {'name': 'Room 102', 'availability': [1, 0, 1, 1]}]
schedule = []

if schedule_courses(courses, teachers, classrooms, schedule):
    print("Course schedule successfully created:")
    for entry in schedule:
        print(entry)
else:
    print("Failed to create a valid course schedule.")