# $ python3 setup.py sdist
# $ twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

import datetime
import math
import calendar
from collections import namedtuple


def convertDateToSQL(oldDate):
  newDate = oldDate[6:] + "-" + oldDate[:2] + "-" + oldDate[3:5]
  return newDate


def dictfetchall(cursor): 
  desc = cursor.description 
  return [
          dict(zip([col[0] for col in desc], row)) 
          for row in cursor.fetchall() 
  ]


def first_day_of_this_month():
  today = datetime.datetime.today().date()
  x = (datetime.datetime.today().date()).replace(day=1)
  x = x.strftime("%m/%d/%Y")
  return x


def first_day_of_this_year():
  x = (datetime.datetime.today().date()).replace(day=1).replace(month=1)
  x = x.strftime("%m/%d/%Y")
  return x


def generateYears():
  list = [
    2000 , 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 
    2010 , 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
    2020 , 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029,
  ]

  return list


def last_day_of_this_month():
  today = datetime.datetime.today().date()
  year = datetime.datetime.today().year
  month = today.month
  last_date = calendar.monthrange(year, month)[1]
  x = today.strftime("%m") + "/" + str(last_date) + "/" + str(year)
  return x


def namedtuplefetchall(cursor):
  desc = cursor.description
  nt_result = namedtuple('Result', [col[0] for col in desc])
  return [nt_result(*row) for row in cursor.fetchall()]


def oneCursorResult(cursor):
  result = namedtuplefetchall(cursor)
  
  if len(result) > 0:
    x = result[0][0]
  else:
    x = ''

  return x


def previousMonth(x):  
  today = datetime.datetime.today().date()
  y = today.year
  m = today.month
  d = today.day
  m = m-x

  pengurang_tahun = 1 + (math.floor((abs(m) / 12)))

  if m < 1:
    y = y - pengurang_tahun
    m = (12 * pengurang_tahun) + m

  newDate = datetime.date(y, m, d)
  return newDate


def previousMonthWithFirstDate(x):
  today = datetime.datetime.today().date()
  y = today.year
  m = today.month
  d = 1
  m = m-x

  pengurang_tahun = 1 + (math.floor((abs(m) / 12)))

  if m < 1:
    y = y - pengurang_tahun
    m = (12 * pengurang_tahun) + m

  newDate = datetime.date(y, m, d)
  return newDate 


def toNumber(value):
  value = value.replace(",", "")
  if(value == ''):
    newValue = 0
  else:
    newValue = float(value)

  return newValue


def userMenuFilter(request, group_code):
  menus = request.session['user_menu']
  data = [x for x in menus if x['group_code'] == group_code]
  return data
