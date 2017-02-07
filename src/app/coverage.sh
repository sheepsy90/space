#!/bin/sh
coverage run manage.py test test
coverage html --include=./*
firefox htmlcov/index.html &
