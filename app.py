#! /usr/bin/python

# This portion of code is fork of gunicorn's example of running
# custom applications.
# Original link - http://gunicorn-docs.readthedocs.org/en/latest/custom.html
# 2009-2015 (c) Benoit Chesneau <benoitc@e-engura.org>
# 2009-2015 (c) Paul J. Davis <paul.joseph.davis@gmail.com>

import multiprocessing
import os
import sys

import gunicorn.app.base
from gunicorn.six import iteritems
from isso import config as isso_config
from isso import make_app

SMTPUSRN = os.getenv('SMTPUSRN', '')
SMTPPASS = os.getenv('SMTPPASS', '')
MAILFROM = os.getenv('MAILFROM', '')
MAILTO = os.getenv('MAILTO', '')
ISSO_CONFIG_FILE = './isso.conf'
ISSO_PATH = next(p for p in sys.path if 'site-packages' in p) + '/isso'
with open(ISSO_CONFIG_FILE, 'r') as f:
    ISSO_CONFIG_STR = f.read()
    ISSO_CONFIG_STR = ISSO_CONFIG_STR.replace('USERNAME', SMTPUSRN)
    ISSO_CONFIG_STR = ISSO_CONFIG_STR.replace('PASSWORD', SMTPPASS)
    ISSO_CONFIG_STR = ISSO_CONFIG_STR.replace('MAILFROM', MAILFROM)
    ISSO_CONFIG_STR = ISSO_CONFIG_STR.replace('MAILTO', MAILTO)
with open(ISSO_CONFIG_FILE, 'w') as f:
    f.write(ISSO_CONFIG_STR)
# with open('./patches/ftqq.patch', 'r') as f:
#     FTQQ_PATCH = f.read()
# with open(ISSO_PATH + '/ext/notifications.py', 'r') as f:
#     file_strs = f.read().split(sep='    def notify(self, thread, comment):', maxsplit=2)
# file_str = file_strs[0] + FTQQ_PATCH + file_strs[1]
# with open(ISSO_PATH + '/ext/notifications.py', 'w') as f:
#     f.write(file_str)

application = make_app(isso_config.load(ISSO_CONFIG_FILE))


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '0.0.0.0:8080',
        'workers': number_of_workers(),
    }
    StandaloneApplication(application, options).run()
