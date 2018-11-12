<a href="https://github.com/vbonvin/ipt_connect"><img style="position: absolute; top: 0; left: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_left_green_007200.png" alt="Fork me on GitHub"></a>

# ipt_connect

A python/django web-based interface to track the grades, compute the rankings and display a lot of interesting statistics on the <a href="https://iptnet.info">International Physicists' Tournament</a>. 

### Status
* Code: working, v2.0, minor display bugs to fix
* Documentation: work in progress
* CI: None

 <a href='http://ipt-connect.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/ipt-connect/badge/?version=latest' alt='Documentation Status' /></a>


## Choose docker image:

### Development
* Run `docker-compose up`
* Open [127.0.0.1:8000/IPTdev/](http://127.0.0.1:8000/IPTdev/)

### Docker without nginx
If you have any web server (for example nginx) on your machine you can use [compose-without-nginx.yml](https://github.com/ijustbsd/ipt_connect/blob/docker/compose-without-nginx.yml). This image use [gunicorn](https://gunicorn.org/) as WSGI server and place `ipt_connect.sock` file into `ipt_connect` directory. Configure your web server for works with it. You can see configuration example for nginx [here](../docker/etc/service.conf).

### Docker with nginx
If you haven't any web server you can use [compose-nginx.yml](../docker/compose-nginx.yml). This image run ipt_connect with nginx proxy and install [Let's Encrypt](https://letsencrypt.org/) certificate.

**How to use:**
* Open [compose-nginx.yml](../docker/compose-nginx.yml) and change things:
  * Set timezone to your local, for example `TZ=UTC`. For more timezone values check /usr/share/zoneinfo directory
  * `LE_EMAIL` should be your email and `LE_FQDN` for domain
* Replace `www.example.com` in [service.conf](../docker/etc/service.conf) by your domain
* Don't forget review your project settings, see [deployment checklist](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/) for more information.


## F.A.Q:

### How to add superuser and sign in to site?
* Run `python manage.py createsuperuser`
* Set username, email address and password.
* Run `python manage.py runserver`
* Open <a href="http://127.0.0.1:8000/admin/">http://127.0.0.1:8000/admin/</a> and sign in.

### How to switch between languages?
Сhange `LANGUAGE_CODE` values in [this](../master/ipt_connect/ipt_connect/settings.py) file to switch the language.  
Available values:
* en-us
* ru

### I added new text to the template. How сan I update language files?
Run `python manage.py makemessages -a -e=html -i=grappelli/*`

### How to compile language files?
Language files compiled automatically when the server starts.

### How to add a new language?
* Run `python manage.py makemessages -l de -e=html -i=grappelli/*` where `de` is the [locale name](https://docs.djangoproject.com/en/2.0/topics/i18n/#term-locale-name) for the message file you want to create.
* Translate all text in the file, which will be create.
* Run application.
