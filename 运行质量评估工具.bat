@echo off
cmd  /k "set PATH=env\Scripts;%PATH% && env\Scripts\activate && cd /d mysite && ..\env\Scripts\python manage.py runserver"
