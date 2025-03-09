import random

class Timetable:
    def __init__(self, days=5, periods_per_day=8):
        self.days = days
        self.periods_per_day = periods_per_day
        self.schedule = [["" for _ in range(periods_per_day)] for _ in range(days)]

    def generate(self, courses, teachers, constraints):
        for day in range(self.days):
            for period in range(self.periods_per_day):
                course = random.choice(courses)
                teacher = random.choice(teachers)
                if self.is_valid(course, teacher, day, period, constraints):
                    self.schedule[day][period] = f"{course} ({teacher})"
                else:
                    self.schedule[day][period] = "Free Period"
        return self.schedule

    def is_valid(self, course, teacher, day, period, constraints):
        # Implement constraints checking logic here
        return True

def generate_timetable(courses, teachers, constraints):
    timetable = Timetable()
    return timetable.generate(courses, teachers, constraints)