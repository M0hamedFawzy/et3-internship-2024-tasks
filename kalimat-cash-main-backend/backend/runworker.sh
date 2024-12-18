#!/bin/sh
celery -A project worker --loglevel=INFO --concurrency=1 -Q kalimatcash -n kalimatcash@%h