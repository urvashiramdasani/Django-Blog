Commands : -

1) To create new virtual environment - virtualenv venv
2) To activate the above created command
C:\Users\Urvashi\Desktop\Practical_10\venv\Scripts\activate.bat
3) Create Project named EmployeeAttendance - django-admin startproject EmployeeAttendance
4) To create an app - python manage.py startapp csv_app
5) Create urls.py in csv_app
6) In settings.py, in installed apps, add 'csv_app'
7) In urls.py of csv_app, import view.home (home is a function). Likewise we can import any function from views.py
8) First apply migrations - python manage.py makemigrations csv_app
9) Then migrate - python manage.py migrate (You will see db.sqlite3 file)
10) Create index.html under template directory and add os.path.join(BASE_DIR, 'template in seetings.py')
11) You have to restart server everytime you make some changes.
