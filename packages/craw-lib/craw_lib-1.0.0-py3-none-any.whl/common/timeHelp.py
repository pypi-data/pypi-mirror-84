#!/usr/bin/python
# coding:utf-8
import re
import time
from datetime import timedelta, datetime

from dateutil import parser
from pytz import timezone

now = datetime.now()


def getOtherDayFormat(day_str, intervals):
    format = '%Y-%m-%d'
    date_arr = day_str.split('-')
    nextDay_str = (
            datetime.datetime(int(date_arr[0]), int(date_arr[1]), int(date_arr[2])) + timedelta(
        days=intervals)).strftime(
        format)
    nextDay_start_int = int(time.mktime(time.strptime(nextDay_str + ' 00:00:00', "%Y-%m-%d %H:%M:%S")))
    nextDay_end_int = int(time.mktime(time.strptime(nextDay_str + ' 23:59:59', "%Y-%m-%d %H:%M:%S")))
    return nextDay_str, nextDay_start_int, nextDay_end_int


def getTodayStart():
    zeroPoint = int(time.time()) - int(time.time() - time.timezone) % 86400
    return zeroPoint


def getTodayEnd():
    zeroToday = getTodayStart()
    lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
    return lastToday


def getCurrentTime():
    return int(time.time())


def stringToNumber(time_string, format='%Y-%m-%d %H:%M:%S'):
    return int(time.mktime(time.strptime(time_string, format)))


def numberToTime(time_number, format='%Y-%m-%d %H:%M:%S'):
    timeArray = time.localtime(time_number)  # 秒数
    otherStyleTime = time.strftime(format, timeArray)
    return otherStyleTime


def getNextdayFormat(intervals):
    # 今天之前或之后N天  day_str 2018-08-08
    day_str = now.strftime('%Y-%m-%d')
    return getOtherDayFormat(day_str, intervals)


def getThisWeek():
    # 本周第一天和最后一天
    format = '%Y-%m-%d'
    this_week_start_str = (now - timedelta(days=now.weekday())).strftime(format)
    this_week_start_int = int(time.mktime(time.strptime(this_week_start_str + ' 00:00:00', "%Y-%m-%d %H:%M:%S")))
    this_week_end_str = (now + timedelta(days=6 - now.weekday())).strftime(format)
    this_week_end_int = int(time.mktime(time.strptime(this_week_start_str + ' 23:59:59', "%Y-%m-%d %H:%M:%S")))
    return this_week_start_str, this_week_start_int, this_week_end_str, this_week_end_int


def getCurrentQuarter():
    # 当前季度
    now_quarter = now.month / 3 if now.month % 3 == 0 else now.month / 3 + 1
    return now_quarter


def datediff(start_date, end_date=''):
    # 计算两个日期之间的差 start_date 2020-05-01
    if end_date == '':
        end_date = now.strftime('%Y-%m-%d')
    (y1, m1, d1) = start_date.split('-')
    (y2, m2, d2) = end_date.split('-')
    d1 = datetime.datetime(int(y1), int(m1), int(d1))
    d2 = datetime.datetime(int(y2), int(m2), int(d2))
    return (d2 - d1).days


def getLastMonth():
    # 上个月第一天和最后一天
    format = '%Y-%m-%d'
    last_month_end = datetime.datetime(now.year, now.month, 1) - timedelta(days=1)
    last_month_end_str = last_month_end.strftime(format)
    last_month_end_int = int(time.mktime(time.strptime(last_month_end_str + ' 00:00:00', "%Y-%m-%d %H:%M:%S")))
    last_month_start_str = (datetime.datetime(last_month_end.year, last_month_end.month, 1)).strftime(format)
    last_month_start_int = int(time.mktime(time.strptime(last_month_start_str + ' 23:59:59', "%Y-%m-%d %H:%M:%S")))
    return last_month_start_str, last_month_start_int, last_month_end_int, last_month_end_str


def getThisMonth():
    # 本月第一天和最后一天
    format = '%Y-%m-%d'
    this_month_start_str = (datetime.datetime(now.year, now.month, 1)).strftime(format)
    this_month_start_int = int(time.mktime(time.strptime(this_month_start_str + ' 00:00:00', "%Y-%m-%d %H:%M:%S")))
    this_month_end_str = (datetime.datetime(now.year, now.month + 1, 1) - timedelta(days=1)).strftime(
        format)
    this_month_end_int = int(time.mktime(time.strptime(this_month_end_str + ' 23:59:59', "%Y-%m-%d %H:%M:%S")))
    return this_month_start_str, this_month_start_int, this_month_end_str, this_month_end_int


def getLastWeek():
    # 上周第一天和最后一天
    format = '%Y-%m-%d'
    last_week_start_str = (now - timedelta(days=now.weekday() + 7)).strftime(format)
    last_week_start_int = int(time.mktime(time.strptime(last_week_start_str + ' 00:00:00', "%Y-%m-%d %H:%M:%S")))
    last_week_end_str = (now - timedelta(days=now.weekday() + 1)).strftime(format)
    last_week_end_int = int(time.mktime(time.strptime(last_week_end_str + ' 23:59:59', "%Y-%m-%d %H:%M:%S")))
    return last_week_start_str, last_week_start_int, last_week_end_str, last_week_end_int


def conv_time(t, format=''):
    allNumbers = re.findall('\d+', t)
    if len(allNumbers) == 0:
        return int(time.time())
    min = int(allNumbers[0])
    if u'秒' in t:
        s = (datetime.now() - timedelta(seconds=min))
    elif u'分钟' in t:
        s = (datetime.now() - timedelta(minutes=min))

    elif u'小时' in t:
        s = (datetime.now() - timedelta(hours=min))

    elif u'天' in t:
        s = (datetime.now() - timedelta(days=min))
    elif format != '':

        s = datetime.strptime(t, format)
    else:
        try:
            timearr = t.split('-')
            if len(timearr) == 3:
                s = datetime.strptime(t, "%Y-%m-%d")
            elif len(timearr) == 2:
                t += ", " + datetime.today().strftime("%Y")
                s = datetime.strptime(t, "%m-%d, %Y")
        except ValueError:
            return 0
    return int(time.mktime(s.timetuple()))


def transTimezone(timeStr):
    dt = parser.parse(timeStr)
    cst_tz = timezone('Asia/Shanghai')
    timeChina = dt.astimezone(cst_tz)
    return int(time.mktime(timeChina.timetuple()))


def time_days_diff_10(timestamp_before_10, timestamp_now_10):
    before_time = datetime.utcfromtimestamp(timestamp_before_10)
    now_time = datetime.utcfromtimestamp(timestamp_now_10)
    return (now_time - before_time).days
