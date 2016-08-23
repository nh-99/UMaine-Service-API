# make sure to pip install beautifulsoup4, mechanze, and pushbullet.py
import mechanize
from random import randint
import re

formId = ""
def select_form(form):
    return form.attrs.get('id', None) == formId

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def get_new_pin(username, password):
    br = mechanize.Browser()
    br.set_handle_refresh(False)
    br.open('https://identity.maine.edu/cas/login?service=https://sousa.umerl.maine.edu:444/myhousing/logon.aspx')

    # Login to CAS
    formId = "Form1"
    br.select_form('form')
    br.form['username'] = username
    br.form['password'] = password
    br.submit()
    if "Enter your Username and Password" in br.response().read():
        return -1
    #print(br.response().read())

    br.select_form(nr=0)
    br.submit(name='btnChangePin')
    #print(br.response().read())

    newPin = random_with_N_digits(4)
    br.select_form(nr=0)
    br.form['txtNewPIN'] = str(newPin)
    br.form['txtConfirmPIN'] = str(newPin)
    br.submit()
    if "Your PIN has been successfully changed!" in br.response().read():
        return newPin
    else:
        return -2
