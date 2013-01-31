# 1Point3Acres Subscriber

## Overview
`1Point3Acres` mail sender. Collect admission post from [1Point3Acres](1point3acres.com/bbs/) forum and form email report periodically.

It has following features:

* Collect admission info automatically
* Collect info according to major
* Stay up-to-date, no repeated message will reach your mail box

Click [here](rainite.com/static/index.html) to subscribe, click [here](rainite.com/static/unsubscribe.html) to unsubscribe.

## How does it work
It parse html retrieved from web page and embed the valid info into mail.(Use cookie to simulate login.) I use crontab to run the `subscriber` every 1 hour.

## TODO

* Use a template engine to form html in email
* Support multi-selection of major
* User authentation
