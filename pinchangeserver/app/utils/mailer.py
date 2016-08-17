import smtplib
import mechanize
import re
import os
from bs4 import BeautifulSoup

def email_pin_change(username, password, newPin):
    toEmail = []
    br = mechanize.Browser()
    br.set_handle_refresh(False)
    br.open('https://identity.maine.edu/cas/login?service=https://sousa.umerl.maine.edu:444/myhousing/logon.aspx')

    # Login to CAS
    br.select_form(nr=0)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()
    #print(br.response().read())

    br.select_form(nr=0)
    br.submit(name='btnCheckYourAssignment')
    #print(br.response().read())

    bs = BeautifulSoup(br.response().read(), "html5lib")
    table = bs.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="gvRoomMates")
    rows = table.findAll(lambda tag: tag.name=='tr')
    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            value = cell.string
            if not bool(re.search(r'\d', value)):
                if "maine.edu" in value:
                    toEmail.append(value)
    send_emails(username, toEmail, newPin)

def send_emails(username, emails, newPin):
    for email in emails:
        fromaddr = os.environ['EMAIL_USERNAME']
        toaddrs  = email
        msg = username + ' has changed your room pin! The new pin is ' + str(newPin)
        username = os.environ['EMAIL_USERNAME']
        password = os.environ['EMAIL_PASSWORD']
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
