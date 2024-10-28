#!/bin/sh

ps -ax | grep -i bok


bokeh serve visualise.py &

sleep 2
open http://localhost:5006/visualise

