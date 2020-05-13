# url-tripline
Python webapp, to watch a URL &amp; send SMS alerts when a change is detected.

## Architecture
ARM (armhf / arm7+ 32bit)

The included prebuilt [selenium](https://github.com/SeleniumHQ/selenium) webdriver/ was built for armhf, which is great for running the project on low-cost 32bit ARM hardware like Raspberry Pi 4. This project will *NOT* run out of the box on Intel/amd64 CPUs (See amd64 [App Engine](https://github.com/bjamesv/url-tripline/tree/gae-custom-runtime1/webdrivers) branch, or replace geckodriver with your own that matches your CPU arch).

## Docker
Dockerfile included to easily build & run application.

1) Edit configuration values:
    * `url.txt` - enter URL to watch
    * `main.py` - enter HTML class name indicating when page is ready to search, HTML class name identifying the page elements to watch, & US phone number to send SMS alerts
    * `alert.py` - enter Twilio SMS id, sending US phone number, & auth token
2) Build: `docker build . -t url-tripline`
3) Run: `docker run -it -ePORT=8080 url-tripline`

Copyright (C) 2020 Brandon J. Van Vaerenbergh
