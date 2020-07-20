Thank you for your interest in contributing to `ipt_connect`!

This file provides some brief advice on how to contribute properly.

# What to contribute?

1. If you've spot a bug, feel free to [open an issue](https://github.com/IPTnet/ipt_connect/issues/new).

2. If you have an idea on how to improve `ipt_connect`, don't hesitate to... yes, [open an issue](https://github.com/IPTnet/ipt_connect/issues/new)!

3. If you want to translate the interface of `ipt_connect` into your language, see [README.md](README.md#how-to-switch-between-languages).

4. Last but not least:
if you know Python, you can do amazing things implementing [issues](https://github.com/IPTnet/ipt_connect/issues).
Some of them are marked as ["good first issue"](https://github.com/IPTnet/ipt_connect/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).
Such issues are a really good point to start from!

*Also, please don't hesitate to add remarks to this guide.*

# Important facts about `ipt_connect`

* The license is [GPLv3](https://en.wikipedia.org/wiki/GNU_General_Public_License#Version_3).

* `ipt_connect` is written in Python 2.7 (see also [#160](https://github.com/IPTnet/ipt_connect/issues/160)).

* It uses Django 1.11 and some other libraries.

* It uses Git for version control anf GitHub for hosting the [public Git repository](https://github.com/IPTnet/ipt_connect).

## Useful links

* [DjangoGirls](https://tutorial.djangogirls.org/en/) - not only for girls!

* [git-scm](https://git-scm.com/book/en/v2) - a great book about Git *(and also a good keyword for googling smth Git-related)*.

# How to contribute?

## Preparing yourself and your PC

1. **Register an account on GitHub**, if you haven't created it yet.
*For some reasons, some people are strictly againt GitHub.
If you are one of them but want to contribute, contact us at nickkolok[at]mail.ru and/or execom[at]iptnet.info*

2. **Install Linux** either into dual-boot or into a virtual machine (of course, if you haven't installed it yet).
As for Linux distributions, we recommend (L/X/K)Ubuntu or Mint.
If you choose to use a virtual machine, we strongly recommend [Oracle VirtualBox](https://www.virtualbox.org/).

*Note: if you are an experienced developer, you (obviously!) may use FreeBSD, ReactOS, macOS or even windows,
but in this case our team will probably unable to help you with OS-specific problems.*

## Setting up the environment

1. Install Python 2.7 and `pip`.
Depending on your distribution, it should be smth like that (for `deb`-based):
```bash
sudo apt-get install python2 pip2
```
(here, and below, and forever - Google is your friend!)

2. Install Git VCS:
```bash
sudo apt-get install git
```

3. Install useful Git-related tools:

*You may skip this step, but is is recommended that you install them.*
*In case of skipping, you will able to do it later whenever you want.*

```bash
sudo apt-get install gitk meld
```

4. Fork [the project](https://github.com/IPTnet/ipt_connect/) on GitHub by pressing the corresponding button (`Ctrl+F` is your friend in case of problems).

5. Clone the forked repository and go to the cloned directory:

*This can be performed from any directory, e.g. the home one `~`.*

Here and below we suppose that your username on GitHub is `phys`.
```bash
git clone https://github.com/phys/ipt_connect.git
cd ipt_connect
```
*You can surely use SSH URLs if you know what they are.*

Since this moment, we suppose that you are in this directory.

*Note: there are a couple of subsequent `ipt_connect` directories. Don't be confused!*

*Note: since 2018-2019, the main branch is called `dev`.*

6. Add the central (upstream) repo to get updates from other contributors:

```bash
git remote add upstream https://github.com/IPTnet/ipt_connect.git
```

The propagation of changes in `ipt_connect` project works in the following way:
	
* To get changes from the upstream repo (that are changes done by others) to your local computer, use
  ```bash
  git fetch upstream
  ```

* To send your local changes to your GitHub repo (and make them public), use
  ```bash
  git push origin branchname1:branchname2
  ```
  where `branchname1` is a name of your local branch and `branchname1` is the name of remote branch
  (the names often are the same, but in general they can be different).

* To suggest the changes from your local repo to be accepted into the main (upstream) repo,
  create a pull request
	  
7. Install the reqired libraries:
```bash
pip install -r requirements.txt
```
*Note: sometimes this should be also done after updating the code from the upstream.*

8. Eventually, run the server!
```bash
cd ipt_connect # Again: it is a subdirectory!
python manage.py runserver
```
Some messages may be shown.
If there are no errors, then just go to the next step.

9. Open [127.0.0.1:8000/IPTdev/](http://127.0.0.1:8000/IPTdev/) in your favourite browser!
If everything went right, you will see a development instance of `ipt_connect` filled  with test data!

## Before changing the code

While changing the code, you should be sure that you're not breaking anything, shouldn't you?
Thus, please do the following steps **before** you edit anything.

1. Running the tests:

```bash
cd ipt_connect
python manage.py test
cd -
```

*Note:* as for now (17 Jul 2020), there are some errors related to `grappelli` and `loginas`.
Just ignore them.
However, there should be **no** errors related to `ipt_connect` itself.

2. Checking availability of the links and resources:

```bash
cd ipt_connect
python manage.py test IPTdev.utils.link_parser
cd -
```

The Internet is constantly changing, new files and pages appear, and old ones are deleted.
And links can change their address. Broken links can damage the site.
An internal link may not work due to erroneous address or removed/non-existing page.
Finally, no one is safe from errors of programmers or administrators.
Each dead link causes negative reaction from users.
This utility crawls all the mentioned links and returns the list of non-working ones.

If you see a dead link before you've made any changes to the files -
please [open an issue](https://github.com/IPTnet/ipt_connect/issues/new).

If you see a dead link (that may be either internal or external) after you've changed the code,
please review your changes :)

3. Creating a dump of HTML code produced:

Until the proper CI is set, we use this simple tool
to check how changes in our `python` code affect the real generated HTML code.


* In a terminal, start the server:
  ```bash
  cd ipt_connect
  python manage.py test
  cd -
  ```
* In another terminal (i.e. without stopping the server), run:
  ```bash
  cd ipt_connect/IPTdev/utils
  python dumper.py
  cd -
  ```
Path to dump will be printed into the terminal

*Note: the dumper uses hash of the last commit to identify the dump.*
*Thus, the dumper shouldn't be used if there are uncommited changes.*

## Changing the code

The recommendations on how to change the codebase are rather general.

* Don't commit changes in database if they're not essential.
  For example, if you've runned `python manage.py createsuperuser`
  to log in and test something, the database will be changed.
  This change should not be commited.

* Always split database changes to a separate commit
  and describe the changes in detail.
  The database is a binary file, so we will not be able to rebase the changes easily.

* If your contribution is related to an issue,
  don't hesitate to mention it like so:
  ```bash
  git commit -m "Add 6-round-fights - see #13666"
  ```
  `see` if for refering, `close` is for closing the issue
  (the issue closes when the pullrequest is merged).

## After the code is changed

When the code is changed and the commit is done,
please check that nothing was broken.
Namely:

* Run tests [(see above)](#before-changing-the-code)

* Check the site for dead links [(also see above)](#before-changing-the-code)

* Create a dump of generated pages [(also see above)](#before-changing-the-code)

* Compare the two dumps (*before* and *after*) your changes

  * using `diff -bBwEZ ...`

  * using `meld`

  * or using your another favourite tool to find difference in HTML code :)

  Please check the difference carefully.

If everything is OK, your pull request is welcome!
