import mechanize
from bs4 import BeautifulSoup

def get_room_info(username, password):
    toReturn = { 'assignment' : {} }
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

    br.select_form(nr=0)
    br.submit(name='btnCheckYourAssignment')
    bs = BeautifulSoup(br.response().read(), "html5lib")
    
    roomNumber = bs.findAll(id='txtAssignment')
    toReturn['assignment']['room'] = roomNumber[0]['value']
    
    roomType = bs.findAll(id='txtRoomType')
    toReturn['assignment']['type'] = roomType[0]['value']
    
    mealPlan = bs.findAll(id='txtMealPlan')
    toReturn['assignment']['mealPlan'] = mealPlan[0]['value']
    
    address1 = bs.findAll(id='txtCampusAddress1')
    address2 = bs.findAll(id='txtCampusAddress2')
    toReturn['assignment']['address'] = (address1[0]['value'].encode('utf-8')).replace('\xc3\x82\xc2\xa0', '') + ', ' + address2[0]['value'].encode('utf-8')
    
    toReturn['assignment']['roommates'] = {}
    table = bs.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id'] == "gvRoomMates")
    rows = table.findAll(lambda tag: tag.name=='tr')
    for row in rows:
        cells = row.findChildren('td')
        if cells:
            for i in range(1,5):
                value = cells[i].string
                if i is 1:
                    toReturn['assignment']['roommates']['firstname'] = value
                elif i is 2:
                    toReturn['assignment']['roommates']['lastname'] = value
                elif i is 3:
                    toReturn['assignment']['roommates']['phone'] = value
                elif i is 4:
                    toReturn['assignment']['roommates']['email'] = value
    
    toReturn['status'] = 'success'
    return toReturn