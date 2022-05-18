#!/usr/bin/env python3

import datetime
import hashlib
import logging
import os
import shutil


class Backup(object):
    now = datetime.datetime.now()
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BACKUPS_DIR = os.path.join(CURRENT_DIR, "backups", str(now.year), str(now.month))
    LOG_FILE = os.path.join(CURRENT_DIR, "backups", "log.txt")

    def __init__(self):
        try:
            os.makedirs(Backup.BACKUPS_DIR)
        except OSError:
            pass
        logging.basicConfig(
            filename=Backup.LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S -",
        )
        self.db_path = os.path.join(Backup.CURRENT_DIR, "db.sqlite3")
        self.db_file = open(self.db_path, "rb")
        if self.is_db_changed():
            logging.info("Starting backup...")
            self.local_backup()
            logging.info("Finished backup.\n")
        else:
            logging.info("Database wasn't changed. Backup not necessary.\n")

    def get_last_db(self):
        """
        Return absolute path to last backup database. If backup doesn't exist return False.
        """
        dbs = []
        for x in os.listdir(Backup.BACKUPS_DIR):
            if x.endswith(".sqlite3"):
                dbs.append((x, os.path.getctime(os.path.join(Backup.BACKUPS_DIR, x))))
        if not len(dbs):
            return False
        last_db = max(dbs, key=lambda x: x[1])
        return os.path.join(Backup.BACKUPS_DIR, last_db[0])

    def is_db_changed(self):
        """
        Return False if current database is the same as last backup database else True.
        """
        last_db_path = self.get_last_db()
        if not last_db_path:
            return True  # If backups doesn't exist return True
        last_db = open(last_db_path, "rb").read()
        return (
            not hashlib.md5(self.db_file.read()).hexdigest()
            == hashlib.md5(last_db).hexdigest()
        )

    def local_backup(self):
        """
        Backup database to local folder.
        """
        now = datetime.datetime.now()
        new_name = "db_{}.sqlite3".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
        try:
            shutil.copyfile(self.db_path, os.path.join(Backup.BACKUPS_DIR, new_name))
        except:
            logging.info("Something wrong, file wasn't copied!")
            return
        logging.info("File was successfully copied.")


if __name__ == "__main__":
    b = Backup()
