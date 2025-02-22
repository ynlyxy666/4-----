from enum import Enum
from typing import Dict, List, Optional

class ScheduleType(Enum):
    WEEKLY = "weekly"     # 每周重复
    SINGLE_WEEK = "odd"   # 单周
    DOUBLE_WEEK = "even"  # 双周

class TimeConflictChecker:
    """时间冲突检测器"""
    
    def check_time_conflict(self, courses: Dict[str, dict], new_course: dict):
        """时间冲突检测"""
        for existing_course in courses.values():
            for new_time_slot in new_course["time"]:
                for existing_time_slot in existing_course["time"]:
                    if self._is_time_overlap(new_time_slot, existing_time_slot):
                        raise ValueError(f"Time conflict detected between {new_course['id']} and {existing_course['id']}")
    
    def _is_time_overlap(self, time_slot1: str, time_slot2: str) -> bool:
        """判断两个时间段是否有重叠"""
        day1, time_range1 = time_slot1.split()
        day2, time_range2 = time_slot2.split()
        if day1 != day2:
            return False
        start1, end1 = time_range1.split('-')
        start2, end2 = time_range2.split('-')
        return not (end1 <= start2 or end2 <= start1)

class CourseManager:
    """课程管理器"""
    
    def __init__(self):
        self.courses: Dict[str, dict] = {}  # {course_id: course_info}
        self.time_conflict_checker: TimeConflictChecker = None  # 初始化时间冲突检查器
    
    def add_course(self, 
                  course_id: str,
                  course_name: str,
                  time_slots: List[str],
                  locations: List[str],
                  teachers: List[str],
                  schedule_type: ScheduleType = ScheduleType.WEEKLY,
                  time_conflict_checker: TimeConflictChecker = None):
        """添加课程接口"""
        if course_id in self.courses:
            raise ValueError(f"Course ID {course_id} already exists")
        
        if time_conflict_checker:
            self.time_conflict_checker = time_conflict_checker
        
        new_course = {
            "id": course_id,
            "name": course_name,
            "time": time_slots,
            "locations": locations,
            "teachers": teachers,
            "type": schedule_type
        }
        if self.time_conflict_checker:
            self.time_conflict_checker.check_time_conflict(self.courses, new_course)
        self.courses[course_id] = new_course
    
    def remove_course(self, course_id: str):
        """删除课程接口"""
        if course_id not in self.courses:
            raise KeyError(f"Course {course_id} not found")
        del self.courses[course_id]
    
    def get_course(self, course_id: str) -> Optional[dict]:
        """课程查询接口"""
        return self.courses.get(course_id)

class CourseScheduler:
    """课表生成器"""
    
    def __init__(self, course_manager: CourseManager):
        self.course_manager = course_manager
    
    def generate_schedule(self, courses: List[dict], daily_limit: int, weekly_days: int) -> Dict[str, List[dict]]:
        """生成课表接口"""
        schedule = {day: [] for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][:weekly_days]}
        
        for course in courses:
            if self._should_include(course, 1):  # Assuming week_num is 1 for simplicity
                for i, time_slot in enumerate(course["time"]):
                    day = time_slot.split()[0]
                    if len(schedule[day]) < daily_limit:
                        schedule[day].append({
                            "time": time_slot,
                            "name": course["name"],
                            "location": course["locations"][i % len(course["locations"])],
                            "teacher": course["teachers"][i % len(course["teachers"])]
                        })
        
        # 按时间排序
        for day in schedule:
            schedule[day].sort(key=lambda x: x["time"])
        return schedule
    
    def _should_include(self, course: dict, week_num: int) -> bool:
        """判断是否应包含当前周"""
        if course["type"] == ScheduleType.WEEKLY:
            return True
        elif course["type"] == ScheduleType.SINGLE_WEEK:
            return week_num % 2 == 1
        elif course["type"] == ScheduleType.DOUBLE_WEEK:
            return week_num % 2 == 0
        return False

# 预留扩展接口示例
class ScheduleExporter:
    """数据导出接口（示例）"""
    @staticmethod
    def export_to_json(schedule: dict):
        """导出为JSON格式"""
        pass
    
    @staticmethod
    def export_to_excel(schedule: dict):
        """导出为Excel格式"""
        pass

# 示例扩展使用方法
if __name__ == "__main__":
    time_conflict_checker = TimeConflictChecker()
    course_manager = CourseManager()
    scheduler = CourseScheduler(course_manager)
    
    # 添加课程
    course_manager.add_course(
        course_id="CS101",
        course_name="Computer Science",
        time_slots=["Mon 9:00-10:30", "Wed 14:00-15:30"],
        locations=["Room 301"],
        teachers=["Dr. Smith"],
        schedule_type=ScheduleType.WEEKLY,
        time_conflict_checker=time_conflict_checker
    )
    
    # 获取课程列表
    courses = list(course_manager.courses.values())
    
    # 生成课表
    schedule = scheduler.generate_schedule(courses, daily_limit=3, weekly_days=5)
    
    # 导出使用
    ScheduleExporter.export_to_json(schedule)
#