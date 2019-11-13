# !/usr/bin/env python
# --------------------------------------------------------------
# File:          calendar.py
# Project:       FDU_Timetable
# Created:       Wednesday, 13th November 2019 5:50:47 pm
# @Author:       Molin Liu, MSc in Data Science
# Contact:          molin@live.cn
# Last Modified: Wednesday, 13th November 2019 5:50:54 pm
# Copyright  © Rockface 2019 - 2020
# --------------------------------------------------------------
from fetchdata import Course
from icalendar import Calendar, Event
from datetime import date
import datetime
import pytz

time_slot_start = {
    0: (8, 00),
    1: (8, 55),
    2: (9, 55),
    3: (10, 50),
    4: (11, 45),
    5: (13, 30),
    6: (14, 25),
    7: (15, 20),
    8: (16, 15),
    9: (17, 10),
    10: (18, 30),
    11: (19, 25),
    12: (20, 20)
}
time_slot_end = {
    0: (8, 45),
    1: (9, 40),
    2: (10, 40),
    3: (11, 35),
    4: (12, 50),
    5: (14, 15),
    6: (15, 10),
    7: (16, 5),
    8: (17, 00),
    9: (17, 55),
    10: (19, 15),
    11: (20, 10),
    12: (21, 5)
}


def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)


def convertDate(week, day, slot):
    tz = pytz.timezone('Asia/Shanghai')
    first_week_in_year = datetime.datetime(2019, 9, 8).isocalendar()[1]
    week += first_week_in_year
    day = int(day)
    GC_date = iso_to_gregorian(2019, week, day+1)
    start_hour, start_min = time_slot_start[int(slot)]
    GC_datetime = datetime.datetime.combine(
        GC_date, datetime.time(hour=start_hour, minute=start_min))
    GC_endTime = GC_datetime+datetime.timedelta(minutes=45)

    return GC_datetime, GC_endTime


def createCourseEvent(course):
    for week in course.available_week:
        for one_course in course.course_time:
            day, time = one_course.split(',')
            print(course.teacher_names)
            start_time, end_time = convertDate(week, day, time)


def createCalendar(course_list):
    cal = Calendar()
    cal['version'] = '2.0'
    cal['prodid'] = '-//Fudan, ©2019 Molin. L//Timetable//CN'
    # print(course_list)
    print(course_list[0])
    createCourseEvent(course_list[0])
    # for course in course_list:
    #event = Event()
    #event.add('summary', course.course_name)
    #event.add('dtstamp', datetime.now())
    # print(course)
    # print(course.teacher_names)
