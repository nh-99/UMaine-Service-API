import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def get_schedule_from_mainestreet(username, password):
    toReturn = {}
    browser = webdriver.Firefox()
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
    
    scheduled_events = []
    for i in range(0, 50):
        try:
            class_name = browser.find_element_by_id('CLASS_NAME$span$' + str(i)).text.splitlines()[0]
            class_type = browser.find_element_by_id('CLASS_NAME$span$' + str(i)).text.splitlines()[1]
            class_location = browser.find_element_by_id('UM_DERIVED_SS_DESCRLONG$' + str(i)).text
            class_times_content = browser.find_element_by_id('DERIVED_SSS_SCL_SSR_MTG_SCHED_LONG$' + str(i)).text
            class_time = re.search('([0-9]?[0-9]:[0-9][0-9](PM|AM) - [0-9]?[0-9]:[0-9][0-9](PM|AM))', class_times_content).group(1)
            class_times = []
            time_c = re.findall('[A-Z][^A-Z]*', class_times_content)
            for t in time_c:
                if "Mo" in t:
                    class_times.append("Monday")
                elif "Tu" in t:
                    class_times.append("Tuesday")
                elif "We" in t:
                    class_times.append("Wednesday")
                elif "Th" in t:
                    class_times.append("Thursday")
                elif "Fr" in t:
                    class_times.append("Friday")
            scheduled_events.append({'name' : class_name, 'type' : class_type, 'location' : class_location, "days" : class_times, "time" : class_time})
        except NoSuchElementException:
            break
    
    toReturn['schedule'] = scheduled_events
    toReturn['status'] = 'success'
    browser.close()
    return toReturn
