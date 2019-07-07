# ipt_connect

A python/django web-based interface to track the grades, compute the rankings and display a lot of interesting statistics on the [International Physicists' Tournament](https://iptnet.info).

* [Status](#status)
* [How to use](#how-to-use)
  * [With Docker](#with-docker)
    * [Development](#development)
    * [Production without nginx](#production-without-nginx)
    * [Production with nginx](#production-with-nginx)
  * [Without Docker](#without-docker)
* [F.A.Q.](#faq)
  * [How to add superuser and sign in to site?](#how-to-add-superuser-and-sign-in-to-site)
  * [How to switch between languages?](#how-to-switch-between-languages)
  * [I added new text to the template. How сan I update language files?](#i-added-new-text-to-the-template-how-сan-i-update-language-files)
  * [How to compile language files?](#how-to-compile-language-files)
  * [How to add a new language?](#how-to-add-a-new-language)
  * [How to run tests?](#how-to-run-tests)
  
## Status
* **Code:** working, v2.0, minor display bugs to fix
* **Documentation:** work in progress
* **CI:** None

[![readthedocs](https://readthedocs.org/projects/ipt-connect/badge/?version=latest)](http://ipt-connect.readthedocs.io/en/latest/?badge=latest)

## How to use

### With Docker

#### Development
This image runs standard Django web server.

* Run `docker-compose up`
* Open [127.0.0.1:8000/IPTdev/](http://127.0.0.1:8000/IPTdev/)

#### Production without nginx
If you have any web server (for example nginx) on your machine you can use [compose-without-nginx.yml](compose-without-nginx.yml). This image uses [gunicorn](https://gunicorn.org/) as WSGI server and places `ipt_connect.sock` file into `ipt_connect` directory. Configure your web server to work with it. You can see configuration example for nginx [here](etc/service.conf). Don't forget to review your project settings, see [deployment checklist](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/) for more information.

#### Production with nginx
If you haven't any web server you can use [compose-nginx.yml](compose-nginx.yml). This image runs ipt_connect with nginx and automatically installs [Let's Encrypt](https://letsencrypt.org/) certificate.

* Open [compose-nginx.yml](compose-nginx.yml) and change things:
  * Set timezone to your local, for example `TZ=UTC`. For more timezone values check `/usr/share/zoneinfo` directory.
  * `LE_EMAIL` should be your email and `LE_FQDN` should be your site domain.
* Replace `www.example.com` in [service.conf](etc/service.conf) by your domain.
* Don't forget to review your project settings, see [deployment checklist](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/) for more information.

### Without Docker

*Not recommended way!*

* Install the requirements `pip install -r requirements.txt`
* Run `python manage.py runserver`
* Open [127.0.0.1:8000/IPTdev/](http://127.0.0.1:8000/IPTdev/)

## F.A.Q:

### How to add superuser and sign in to site?
* Run `python manage.py createsuperuser`
* Set username, email address and password.
* Run `python manage.py runserver`
* Open [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and sign in.

### How to switch between languages?
Сhange `LANGUAGE_CODE` values in [this](ipt_connect/ipt_connect/settings.py) file to switch the language.
Available values:
* en-us
* ru

### I added new text to the template. How сan I update language files?
Run `python manage.py makemessages -a -e=html -i=grappelli/*`

### How to compile language files?
Language files are compiled automatically when the server starts.

### How to add a new language?
* Run `python manage.py makemessages -l de -e=html -i=grappelli/*` where `de` is the [locale name](https://docs.djangoproject.com/en/2.0/topics/i18n/#term-locale-name) for the message file you want to create.
* Translate all text in the file, which will be create.
* Run application.

### How to start a new tournament?
* Run `python manage.py flush`
* Sign in as superuser and add new participants, jury members and etc.

This command just deletes all the data of current tournament(s).
If you want to start a new tournament in adition to existent,
read below.

### What if I have the list of participants somewhere else?
Then you can avoid inserting the participants and jurors  by hand.
Log in as superuser and navigate to <a href="http://127.0.0.1:8000/IPTdev/upload_csv/">http://127.0.0.1:8000/IPTdev/upload_csv/</a>.
Select a CSV file and click `Upload`.
Note that the format of CSV file is hardcoded in `views.py`.
Don't hesitate to adjust it for your needs!

### How to add (clone) a tournament?
`./clone-instance.sh IPTdev IPT2019`
`IPTdev` is the name of existing instance.
`IPT2019` is the name of instance to be created.

Look to the commits being done to see the details.

There are three main parts of the new tournament:
* `IPT2019` folder with the code
* Records in `ipt_connect/urls.py` and `ipt_connect/settings.py`
* Tables in the database

If you are deploying an instance, which you created locally, to the remote server -
then you have to do the required steps manually.
Just create the instance locally and look at the commits which wil be created.

Notice: this clones only structure of the tournament,
i.e. you have an empty table for teams, no registered jurors, etc.

### How to see modifications in html code after new commit?

Sometimes change in backend code of product can affect on frontend part.
We'll see, have affected on pages?

Dumper - utility for collect all pages

* Install the requirements `pip install -r requirements.txt`

* To do dump:
  * Run `python manage.py runserver` 
  * Run `python manage.py test IPTdev.utils.dumper`
In terminal you will see path to dump

* Compare dumps:
  * Run `python manage.py test IPTdev.utils.diff_html`
  (Do not need to run server) 
  * Select folders with dump (if you have Python-tk) or input hash commits
In terminal you will see path to difference 

### How to run tests?

* Run `python manage.py test` 

### Link checking
* Run `python manage.py test IPTdev.utils.link_parser`

The Internet is constantly changing, new files and pages appear, and old ones are deleted.
And links can change their address. Broken links can damage the site.
An internal link may not work due to erroneous address or removed/non-existing page.
Finally, no one is safe from errors of programmers or administrators.
Each dead link causes negative reaction from users.
This utility crawls all the mentioned links and returns the list of non-working ones.

