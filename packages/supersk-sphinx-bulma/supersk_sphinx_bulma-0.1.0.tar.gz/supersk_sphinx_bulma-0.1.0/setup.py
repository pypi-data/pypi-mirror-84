#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    entry_points = {
        'sphinx.html_themes': [
            'supersk-sphinx-bulma = supersk_sphinx_bulma',
        ]
    }
)
