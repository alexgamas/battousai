#!/bin/bash

ffmpeg -i video.mp4 -r 1/5 ./images/filename%03d.jpg
