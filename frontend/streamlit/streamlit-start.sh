#! /usr/bin/env bash
set -e

aws s3 sync s3://cephalo/images-512/ ./input/cepahlo

streamlit run streamlit-app.py
