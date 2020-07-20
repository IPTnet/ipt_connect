**This is a draft. It may be impolite or toxic somewhere. Sorry in advance!**


Thank you for your interest in contributing to `ipt_connect`!

This file provides some brief advice on how to contribute properly.

# What to contribute?

1. If you've spot a bug, feel free to [open an issue](https://github.com/IPTnet/ipt_connect/issues/new).

2. If you have an idea on how to improve `ipt_connect`, don't hesitate to... yes, [open an issue](https://github.com/IPTnet/ipt_connect/issues/new)!

3. If you want to translate the interface of `ipt_connect` into your language, see [README.md](README.md).

4. Last but not least:
if you know Python, you can do amazing things implementing [issues](https://github.com/IPTnet/ipt_connect/issues).

*Also, please don't hesitate to add remarks to this guide.*

# Important facts about `ipt_connect`

* The license is [GPLv3](https://en.wikipedia.org/wiki/GNU_General_Public_License#Version_3).

* `ipt_connect` is written in Python 2.7 (see also [#160](https://github.com/IPTnet/ipt_connect/issues/160)).

* It uses Django 1.11 and some other libraries.

* It uses Git for version control anf GitHub for hosting the [public Git repository](https://github.com/IPTnet/).

## Useful links

* [DjangoGirls](https://tutorial.djangogirls.org/en/) - not only for girls!

* [git-scm](https://git-scm.com/book/en/v2) - a great book about Git *(and also a good keyword for googling smth Git-related)*.

# How to contribute?

## Preparing yourself and your PC

1. *Register an account on GitHub*, if you haven't created it yet.
*For some reasons, some people are strictly againt GitHub.
If you are one of them but want to contribute, contact us at nickkolok[at]mail.ru and/or execom[at]iptnet.info*

2. *Install Linux* either into dual-boot or into a virtual machine (of course, if you haven't installed it yet).
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

*You may skip the step, but is is recommended that you install them.*
*In case of skipping, you are able to do it later.*

```bash
sudo apt-get install gitk meld
```

4. Fork the project on GitHub by pressing the corresponding button (`Ctrl+F` is your friend in case of problems).

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
