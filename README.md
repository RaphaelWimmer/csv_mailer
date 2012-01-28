csv_mailer.py
=============

Send customized emails to recipients in a CSV file

(c) 2008 Raphael Wimmer <raphael.wimmer@ifi.lmu.de>

This code is in the public domain - use it however you like
 
Take caution when sending out mass mailings using this script. 

Do not use this script for spamming.

Features
--------

* fills an email template with data from a CSV list
* short, clean and customizable
* requires some customization for a specific task
* double protection against mistakes
* TLS and authentication for SMTP
* UTF-8 - should work for all languages


How to use
----------

* adjust mail_template.txt 
* prepare CSV list (see example)
* customize script so that it replaces placeholders in the template with data from the CSV file or other sources
* send e-mails
  * do a dry-run first (DRY_RUN=1), no email will actually be sent
  * test in safe mode (DRY_RUN=0 and SAFE_MODE=1) - all emails will be sent to one specified address (ideally your own address).
  * if everything seems ok, disable SAFE_MODE and run the script again. 

Ideally, you should do all your local modifications in separate git branches. Then you can pull updates to this script without clashes with your existing modifications.

Links
-----

* Similar project on github: https://github.com/qoda/python-mailer
* First version of code: http://my.opera.com/raphman/blog/2008/05/13/python-script-for-sending-out-bulk-password-e-mails

