#!/bin/bash

if [ $# -ne 1 ]; then
  echo "need [appname]"
  exit 1
fi

django-admin startapp $1
