
1>
Start by installing python first on the local system
 sudo apt install python3-pip
 sudo apt install python3

2>
Install Django using python and then setup the bashrc
pip install django

Setup the envornment for the python to use update the .bashrc
vi ~/.bashrc
export PATH="/usr/local/bin:$PATH"
#save the file :wq

source .bashrc
(if your still not able to run django-admin command reloin to ubuntu)

3>
Create a new Django project named "mini-python":
#django-admin startproject mini_python
#cd mini_python

4>
Create a Simple Django App:
Inside the project directory, create a new Django app called minipython:
#python manage.py startapp minipython

5>
Add the app to the project settings. Open mini_python/settings.py and add 'minipython' to the INSTALLED_APPS list:

INSTALLED_APPS = [
    ...
    'minipython',
]

6>
Create a simple view in minipython/views.py:

from django.http import HttpResponse
def index(request):
    return HttpResponse("Welocme to Cloud Command Classroom mini-python Django application!")

7>
Configure a URL route for the view. Create a urls.py file in the minipython directory and add the following:

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

8>
Include the minipython app URLs in the main project URL configuration. Open mini_python/urls.py and update it:

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('minipython.urls')),
]

9>
Run and test if the django working on the local frist
#python3 manage.py runserver

10>
Now will start with the docker file from here check the dockerfile for further configurations

