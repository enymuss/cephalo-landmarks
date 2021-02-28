#! /usr/bin/env bash
set -e

aws s3 sync s3://cephalo/images-512/ app/nn_models/cephalo/inputs
aws s3 sync s3://cephalo/models/ app/nn_models/cephalo/models

python /app/app/celeryworker_pre_start.py

celery worker -A app.worker -l info -Q main-queue -c 1
