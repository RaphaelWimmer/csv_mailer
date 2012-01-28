#!/usr/bin/python
# -*- coding: utf-8 -*-

# csv_mailer.py 
# Send customized emails to recipients in a CSV file
#
# (c) 2008 Raphael Wimmer <raphael.wimmer@ifi.lmu.de>
# This code is in the public domain - use it however you like

# Take caution when sending out mass mailings using this script. 
# If in doubt, ask the administrator of your email server.
# Do not use this script for spamming.

import smtplib
import csv

# CONFIG
CSVFILE = "recipients.csv"
TEMPLATE = "mail_template.txt"

SENDER = '"Me" <test@example.com>'
SMTP_SERVER = 'mail.example.com'
SMTP_PORT = 587

USE_TLS = 1 # for encrypted connection to SMTP server set to 1
AUTH_REQUIRED = 1 # if you need to use SMTP AUTH set to 1
SMTP_USER = 'me'  # for SMTP AUTH, set SMTP username here
SMTP_PASS = 'password'  # for SMTP AUTH, set SMTP password here

# You have to set the following two variables to 0 
# in order to actually send the e-mails to the recipients!
DRY_RUN = 1 # do not actually send e-mails but print what would have happened
SAFE_MODE = 1 # if set, all mails will be sent to RECIPIENTS instead of the address specified in the csv file.
RECIPIENTS = ['test@example.com']

#if you have a semicolon-delimited file, also add dialect to reader (see below)
#csv.register_dialect("semicolon", delimiter=';', quoting=csv.QUOTE_NONE)



######## START ########

template = open(TEMPLATE, "r")
csvfile  = open(CSVFILE, "r")

mail_template = template.read()
csv_reader = csv.DictReader(csvfile) # add 'dialect="semicolon"' if necessary

######## Open SMTP session ########
smtpresult = 0  # define it so we do not get an error during DRY_RUN
if not DRY_RUN:
    print "Opening SMTP session"
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    #session.set_debuglevel(1)
    session.ehlo()
    if USE_TLS and session.has_extn("STARTTLS"): # not tested!
        session.starttls()
        session.ehlo()
    if AUTH_REQUIRED:
        session.login(SMTP_USER, SMTP_PASS)

######## Send emails ########
for row in csv_reader:
    # adapt these fields to your needs
    surname = row["Last Name"]
    givenname = row ["First Name"]
    email = row["Email"]
    id = row["ID"]
    recipient = "\"" + givenname + " " + surname + "\" " + "<" + email + ">"
    
    # add your own business logic here, e.g. randomly generating a password

    print "Sending mail to " + email
    mssg = mail_template.replace("$NAME$", givenname + " " + surname)
    mssg = mssg.replace("$SENDER$", SENDER)
    mssg = mssg.replace("$RECIPIENT$", recipient)
    mssg = mssg.replace("$EMAIL$",email)
    mssg = mssg.replace("$ID$", id)
    
    if SAFE_MODE:
        recipients = RECIPIENTS
        print "[SAFE MODE] Sending email to " + recipients[0]
        mssg = mssg + "\r\nThis message would have been sent to " + email
    else:
        recipients = [email]
        
    if DRY_RUN:
        print "[DRY RUN] Sending mail to " + recipients[0]
        print
        print mssg
        print
        print "################################################################################"
    else:
        smtpresult = session.sendmail(SENDER, recipients, mssg)

    if smtpresult:
        errstr = ""
        for recip in smtpresult.keys():
            errstr = """Could not deliver mail to: %s

    Server said: %s
    %s

    %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
        raise smtplib.SMTPException, errstr

    print
