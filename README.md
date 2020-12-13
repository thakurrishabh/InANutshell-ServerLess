# Inanutshell
 store.listen.learn
 
Recorded demos of our Web Service and Alexa skill:

https://www.dropbox.com/s/082ealj9ppema3k/inanutshell_demo.mp4?dl=0

https://www.dropbox.com/s/mhyl3uqrnf2qovx/alexa_demo.MP4?dl=0

inanutshell1 is a django package with templates, models, views and forms AND NEED TO UPDATE API KEYS AND MONGODB SRV

First you need to install virtual environment and then libraries from requirements


LINUX

$ virtualenv <env_name>

$ source <env_name>/bin/activate

$ (<env_name>)$ pip install -r path/to/requirements.txt


WINDOWS

$ virtualenv <env_name>

$ zappaenv1\\\Scripts\\\activate.bat

$ (<env_name>)$ pip install -r path/to/requirements.txt


DJANGO COMMANDS TO MAKE ANY CHANGES

$ python manage.py makemigrations

$ python manage.py migrate

$ python manage.py runserver 


TO UPDATE STATIC FILES TO LAMBDA

$ python manage.py collectstatic --no-input

ZAPPA COMMANDS

$ zappa init

$ zappa deploy dev

$ zappa update dev

$ zappa certify dev

AWS lamda and Alexa files are also provided in zip



