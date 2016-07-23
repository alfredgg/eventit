#!/usr/bin/env python
# -*- coding: utf-8 -*-


def create():
    from data_model import db
    db.create_all()


def reset():
    from data_model import db
    db.drop_all()

if __name__ == '__main__':
    create()