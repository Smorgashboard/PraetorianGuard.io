﻿
# PraetorianGuard.IO


Vulnerability assement tool for MSPs and small businesses.

This is not the complete version but more of a basic framework.

Tool is built with Django Framework for Python3. It utilizes a PostgreSQL db backend. Currently that is hosted in AWS but could be done locally. 

There are four main components.

1) OSINT - Utilizing various API's for leaked databases this tool will check for email/password that have been pwned. It will also check based on Domain name IE all example.com emails and cooresponding PWs.
2) Phishing - This enables users to send phishing emails to clients. Utilizing a hosted 1x1 pixel we are able to see if the email is opened. Email templates contain links that will track if a user clicks the link. Custome GUIDs track which user is clicking which link and which user is opening emails. Gmail will auto open and download pixels so we are currently checking the headers for google agent and discarding those results.
3) Vulnerability Assement - This is currently linked to a Lambda function on AWS that points to a Compute instance with a listener. That compute instance fires off a vulnerability assessment on the target machine. That assessment is done through a number of various scripts not in this repo that run tools like (nmap, nuclei, sqlmap etc...)
4) WPScan - Wordpress Scanner for checking known plugin vulns on a site


Dashboard views are for MSP based dashboards and views of their client lists.
Reports is for generating reports.
