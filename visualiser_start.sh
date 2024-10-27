#!/bin/sh

bokeh serve visualise.py &

sleep 2
open http://localhost:5006/visualise

