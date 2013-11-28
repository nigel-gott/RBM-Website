RBM-Website
===========
Django website for RBM Library. 

Run install.sh to create virtual env, install required packages into it, clean database and setup git hooks. 

!!! Important !!!
===========
Make sure you always have the virtual enviroment activated when working on the website.
Run activate or "source venv/bin/activate" or "source venv/bin/activate.csh" to activate the virtual enviroment.

The git hooks will update requirements.txt every time you commit with whatever packages you have installed to pip.  

Running the Website:
===========

Once in the virtual environment, run 'python manage.py runserver' to setup the local server. If it runs correctly, it will output the address of the home page.

Running Celery:
===========
Celery is used to run the background tasks such as training. To edit these tasks, look at tasks.py. To start celery, run the following: ```python manage.py celeryd -v 2 -B -s celery -E -l INFO```

I'm not 100% on what all these arguments do and will look into them soon.


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

TODO:
===========
- Add page authentication
- Complete celery training
- Add information page
- Train static DBNs (Digits, Characters)
- Add classifier on home page
- Setup RabbitMQ for celery
- Find a better way of storing files
- Clean up javascript/python
- Make HTML pages and elements look nice
- Document and Comment code
- Prepare library to download

What are all these words, help!
===========
Do the tutorial: https://docs.djangoproject.com/en/1.5/intro/install/

Learn how to use virtualenv: http://codekarate.com/blog/using-virtual-environments-django

https://docs.djangoproject.com/ provides a really good documentation for django.




