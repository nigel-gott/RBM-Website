RBM-Website
===========
Django website for RBM Library. 

How to install
==============

1. Ensure you have git, python and virtualenv installed on your system.
2. Clone this repository to the desired location.
3. Setup a database and configure the default database on line 25 of rbm\_website/settings.py, by default it looks for a postgresql with a database named dbn\_database, a user called postgres with the password postgres.
4. Run install.sh to create virtual env, install required packages into it, clean database and setup git hooks. 
5. Run both run\_webserver.sh and run\_celery.sh in seperate terminals. The celery terminal will display output when it trains an RBM and any errors related to that.
6. Visit the url shown by run\_webserver.sh to see the site. 

Some configuration options
===========
In rbm\_website you can configure FLIPPED\_DBNS to be the list of id's of rbms who you want black pixels to be treated as white and vice versa.

You can also configure which DBN displays on the front page by editting HOME\_DBN with the corrosponding dbn's id.

!!! Important !!!
===========
Make sure you always have the virtual enviroment activated when working on the website.
Run activate or "source venv/bin/activate" or "source venv/bin/activate.csh" to activate the virtual enviroment.

The git hooks will update requirements.txt every time you commit with whatever packages you have installed to pip.  

Running the Website:
===========

Once in the virtual environment, run 'python manage.py runserver' to setup the local server. If it runs correctly, it will output the address of the home page. Alternatively you can just use run\_webserver.sh to do the same thing.

Running Celery:
===========
Celery is used to run the background tasks such as training. To edit these tasks, look at tasks.py. To start celery, run the following: ```python manage.py celeryd -v 2 -B -s celery -E -l INFO```


Project Structure 
===========
```
rbm_website/      - The Django project
  apps/           - The Django apps (created by us, a Django project ideally consists of a bunch of little apps)
    rbm/          - The main section of the website. Contains the DBN models, views and HTML templates
      static/     - Contains the static files for use by the RBM app
    users/        - The users apps that maintains user accounts. Not much need to edit this section.
  libs/           - 3rd party librarys
    rbm_lib/      - The RBM Library git repo as a sub module 
  settings.py     - Project level settings
  urls.py         - Project level urls
  static/         - Contains global static files like fonts, CSS and javascript files.
hooks/            - Git hooks
  pre-commit      - Update requirements.txt with pip freeze
  post-merge      - Install all requirements in requirements.txt (someone else might have added new packages)
install.sh        - Sets up virtual enviroment, project requirements, git hooks, submodules.
requirements.txt  - Required python packages, use pip freeze to see what is currently installed in your venv. 
```


What are all these words, help!
===========
Do the tutorial: https://docs.djangoproject.com/en/1.5/intro/install/

Learn how to use virtualenv: http://codekarate.com/blog/using-virtual-environments-django

https://docs.djangoproject.com/ provides a really good documentation for django.




