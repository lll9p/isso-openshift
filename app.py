#! /usr/bin/python

# This portion of code is fork of gunicorn's example of running
# custom applications.
# Original link - http://gunicorn-docs.readthedocs.org/en/latest/custom.html
# 2009-2015 (c) Benoit Chesneau <benoitc@e-engura.org>
# 2009-2015 (c) Paul J. Davis <paul.joseph.davis@gmail.com>

import os
import multiprocessing

import gunicorn.app.base
from gunicorn.six import iteritems
from isso import make_app
from isso import config as isso_config

application = make_app(isso_config.load('isso.conf'))

print('LOADING MODULE %s' % __file__)


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
        'bind': ':8080',
        'workers': number_of_workers(),
    }
    StandaloneApplication(application, options).run()
