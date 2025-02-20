from enum import Enum
from typing import Dict, List, Optional

class ScheduleType(Enum):
    WEEKLY = "weekly"     # 每周重复
    SINGLE_WEEK = "odd"   # 单周
    DOUBLE_WEEK = "even"  # 双周

class CourseSchedule:
    """课表生成器（核心类）
    
    功能：
    - 课程增删改查
    - 时间冲突检测
    - 多种排课模式支持
    - 课表可视化生成
    
    预留接口：
    - 数据持久化接口
    - 外部系统对接接口
    - 自定义规则引擎接入点
    """
    
    def __init__(self):
        self.courses: Dict[str, dict] = {}  # {course_id: course_info}
        self.schedule: List[dict] = []
    
    def add_course(self, 
                  course_id: str,
                  course_name: str,
                  time_slots: List[str],
                  location: str,
                  teacher: str,
                  schedule_type: ScheduleType = ScheduleType.WEEKLY):
        """添加课程接口
        Args:
            course_id: 课程唯一标识
            time_slots: 时间段列表 ["Mon 9:00-10:30", "Wed 14:00-15:30"]
            schedule_type: 排课模式
        """
        if course_id in self.courses:
            raise ValueError(f"Course ID {course_id} already exists")
        
        new_course = {
            "id": course_id,
            "name": course_name,
            "time": time_slots,
            "location": location,
            "teacher": teacher,
            "type": schedule_type
        }
        self._check_time_conflict(new_course)
        self.courses[course_id] = new_course
    
    def remove_course(self, course_id: str):
        """删除课程接口"""
        if course_id not in self.courses:
            raise KeyError(f"Course {course_id} not found")
        del self.courses[course_id]
    
    def get_course(self, course_id: str) -> Optional[dict]:
        """课程查询接口"""
        return self.courses.get(course_id)
    
    def generate_schedule(self, week_num: int = 1) -> Dict[str, List[dict]]:
        """生成课表接口
        Args:
            week_num: 第N周课表（用于单双周模式）
        Returns:
            按星期分组的课程表结构
        """
        schedule = {"Mon": [], "Tue": [], "Wed": [], "Thu": [], "Fri": [], "Sat": [], "Sun": []}
        
        for course in self.courses.values():
            if self._should_include(course, week_num):
                for time_slot in course["time"]:
                    day = time_slot.split()[0]
                    schedule[day].append({
                        "time": time_slot,
                        "name": course["name"],
                        "location": course["location"],
                        "teacher": course["teacher"]
                    })
        
        # 按时间排序
        for day in schedule:
            schedule[day].sort(key=lambda x: x["time"])
        return schedule
    
    def _check_time_conflict(self, new_course: dict):
        """时间冲突检测（内部方法）"""
        # 实现逻辑...
    
    def _should_include(self, course: dict, week_num: int) -> bool:
        """判断是否应包含当前周（内部方法）"""
        # 实现单双周逻辑...

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
    scheduler = CourseSchedule()
    
    # 添加课程
    scheduler.add_course(
        course_id="CS101",
        course_name="Computer Science",
        time_slots=["Mon 9:00-10:30", "Wed 14:00-15:30"],
        location="Room 301",
        teacher="Dr. Smith",
        schedule_type=ScheduleType.WEEKLY
    )
    
    # 生成课表
    schedule = scheduler.generate_schedule()
    
    # 导出使用
    ScheduleExporter.export_to_json(schedule)