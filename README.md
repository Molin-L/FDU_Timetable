# FDU Timetable

Timetable exporter for FDU
自动登录教务系统读取课表，导出为.ics文件
Automatically login to jwfw.fdu.edu.cn, export as ics file.

**Log:**2019-11-14 00:43:20: **Finish**

# Setup
Download this repo, add your username and password to the buttom of `fetchdata.py`, then run`python3 fetchdata.py`

尽量以邮件的方式发送生成的`fdu_timetable.ics`至你的邮箱，iOS使用系统默认邮箱打开
# Overview
## Login
教务系统登录：`fdulogin.py`

## Table Retrieve
Implemented in: `fetchdata.py`

## Convert to .ics file
Implemented in: `fileman.py`

# License
See `LICENSE` for more information.