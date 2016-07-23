#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eventit import app

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8080"),
        debug=True
    )