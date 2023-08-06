# $ python3 setup.py sdist
# $ twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

def convertDateToSQL(oldDate):
  newDate = oldDate[6:] + "-" + oldDate[:2] + "-" + oldDate[3:5]
  return newDate


def dictfetchall(cursor): 
  desc = cursor.description 
  return [
          dict(zip([col[0] for col in desc], row)) 
          for row in cursor.fetchall() 
  ]