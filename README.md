# FDU Timetable

This project reads timetable from your jwfw.fdu site, then export to calendar.

用于复旦大学课表导入日历

Still under constructing 2019-11-13

# Setup
[TODO]

# Overview
## Login
1. 登录页面有`needcaptcha`检查，时间戳是GMT+0的秒数;
2. 登录需要手动重定向获取cookies。在自动重定向的状态下最后得到的页面仍然是登录页面，而且状态码是 `200`，不是期望得到的 `302`，不过可以通过`response.history`查看中间是否有`302`状态码;

**登录部分已完成**

## Table Retrieve
[TODO]

## Convert to .ics file
[TODO]

## Location
*Add location to calendar event*
[TODO]
# License
