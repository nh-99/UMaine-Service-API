import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_isbns_from_mainestreet(username, password):
    browser = webdriver.PhantomJS()
    url = 'https://peportal.maine.edu/psp/PAPRD89/EMPLOYEE/EMPL/h/?tab=PAPP_GUEST'
    browser.get(url)
    time.sleep(2)

    # Auth to MaineStreet
    usernameInput = browser.find_element_by_id('userid')
    usernameInput.send_keys(username)
    passwordInput = browser.find_element_by_id('pwd')
    passwordInput.send_keys(password)
    passwordInput.send_keys(Keys.ENTER)
    time.sleep(1)

    url = 'https://peportal.maine.edu/psp/PAPRD89/EMPLOYEE/EMPL/s/WEBLIB_ACCESS.ACCESS_PERMISSION.FieldFormula.IScript_GOTO_CS_ST?TYPE=c&NODE=CSPRDST&MENU=SA_LEARNER_SERVICES&COMP=SSS_STUDENT_CENTER&PAGE=SSS_STUDENT_CENTER&FolderPath=PORTAL_ROOT_OBJECT.UM_STUDENT_SELF_SEVICE.UM_STUDENT_CENTER2&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder'
    browser.get(url)
    time.sleep(3)

    browser.switch_to_frame('ptifrmtgtframe')
    class_schedule = browser.find_element_by_name('DERIVED_SSS_SCR_SSS_LINK_ANCHOR1')
    class_schedule.click()
    time.sleep(3)

    textbook_info_url = browser.find_element_by_id('UM_DERIVED_SR2_UM_TEXTBOOK_URL').get_attribute('href')
    browser.get(textbook_info_url)
    time.sleep(3)

    textbook_isbns = []
    for potential_isbn in browser.find_elements_by_class_name('bkD'):
        textbook_isbns.append(potential_isbn.text)

    isbns = [int(s) for s in textbook_isbns if s.isdigit()]
    browser.close()
    return isbns

def get_textbook_prices(isbns):
    browser = webdriver.PhantomJS()
    toReturn = {}
    for isbn in isbns:
        url = 'https://www.textsurf.com/details/' + str(isbn)
        browser.get(url)

        pricesForBook = []
        for price in browser.find_elements_by_class_name('btn-success'):
            if re.search('\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})', price.text) is not None:
                print(price.text)
                pricesForBook.append([price.text, price.get_attribute('href')])
        toReturn[isbn] = pricesForBook
    time.sleep(1)
    browser.close()
    return toReturn
