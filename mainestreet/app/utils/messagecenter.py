import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def get_messages_from_mainestreet(username, password):
    toReturn = {}
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
    class_schedule = browser.find_element_by_name('UM_DERIVED_SSS_UM_SS_MCTR_COMM_LC$4$')
    class_schedule.click()
    time.sleep(3)
    
    messages = []
    for i in range(0, 50):
        try:
            message_description = browser.find_element_by_id('UM_COMM_ID$' + str(i))
            message_date = browser.find_element_by_id('UM_MCTR_STDNTVW_START_DATE$' + str(i))
            message_read = browser.find_element_by_id('UM_MCTR_STDNTVW_UM_OPENED_COMM_FLG$' + str(i))
            message_viewed = False
            if message_read.text == 'Y':
                message_viewed = True
            messages.append({'description' : message_description.text, 'date' : message_date.text, 'viewed' : message_viewed})
        except NoSuchElementException:
            break
    
    toReturn['messages'] = messages
    toReturn['status'] = 'success'
    browser.close()
    return toReturn
