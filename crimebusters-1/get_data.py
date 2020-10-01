### Getting data from UCR for crimebusters ###
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

def get_state_data(state, csv_filename):
    driver = webdriver.Firefox()
    driver.get('https://www.ucrdatatool.gov/Search/Crime/State/StatebyState.cfm')
    if state != 'United States-Total':
        c = "[contains(text(), '" + state + "')]"
        state_object = driver.find_elements_by_xpath("//select"+\
                       "[@name='StateId']/*"+c)[0]
    else:
        state_object = driver.find_elements_by_xpath("//select"+\
                       "[@name='StateId']/option[@value='52']")[0]
    state_object.click()
    for choice in range(1, 5):
        string = str(choice)
        data_object = driver.find_elements_by_xpath("//select[@name="+\
                      "'DataType']/option[@value= "+string+"]")[0]
        data_object.click()
    year_start = driver.find_elements_by_xpath("//select[@name='YearStart']"+\
                "/option[@value='2001']")[0]
    year_start.click()
    year_end = driver.find_elements_by_xpath("//select[@name='YearEnd']"+\
                "/option[@value='2014']")[0]
    year_end.click()
    next_page = driver.find_elements_by_xpath("//input[@name='NextPage' and "+\
                "@type='submit']")[0]
    next_page.click()
    yrs = driver.find_elements_by_xpath("//td[@headers='year']")
    pops = driver.find_elements_by_xpath("//td[@headers='population']")
    v_nums = driver.find_elements_by_xpath("//td[@headers="+\
                  "'num vcrime1 vctot']")
    murd_nums = driver.find_elements_by_xpath("//td[@headers="+\
                 "'num vcrime1 murd']")
    rape_nums = driver.find_elements_by_xpath("//td[@headers="+\
                      "'num vcrime1 rape']")
    rob_nums = driver.find_elements_by_xpath("//td[@headers="+\
                   "'num vcrime1 rob']")
    aslt_nums = driver.find_elements_by_xpath("//td[@headers="+\
                        "'num vcrime1 aggr']")
    p_nums = driver.find_elements_by_xpath("//td[@headers="+\
                          "'num pcrime1 pctot']")
    burg_nums = driver.find_elements_by_xpath("//td[@headers="+\
                    "'num pcrime1 burg']")
    larc_nums = driver.find_elements_by_xpath("//td[@headers="+\
                   "'num pcrime1 larc']")
    mv_nums = driver.find_elements_by_xpath("//td[@headers="+\
                    "'num pcrime1 mvtheft']")
    v_rts = driver.find_elements_by_xpath("//td[@headers="+\
                   "'rate vcrime2 vctot2']")
    murd_rts = driver.find_elements_by_xpath("//td[@headers="+\
                  "'rate vcrime2 murd2']")
    rape_rts = driver.find_elements_by_xpath("//td[@headers="+\
                       "'rate vcrime2 rape2']")
    rob_rts = driver.find_elements_by_xpath("//td[@headers="+\
                    "'rate vcrime2 rob2']")
    aslt_rts = driver.find_elements_by_xpath("//td[@headers="+\
                         "'rate vcrime2 aggr2']")
    p_rts = driver.find_elements_by_xpath("//td[@headers="+\
                    "'rate pcrime2 pctot2']")
    burg_rts = driver.find_elements_by_xpath("//td[@headers="+\
                     "'rate pcrime2 burg2']")
    larc_rts = driver.find_elements_by_xpath("//td[@headers="+\
                    "'rate pcrime2 larc2']")
    mv_rts = driver.find_elements_by_xpath("//td[@headers="+\
                     "'rate pcrime2 mvtheft2']")
    list_of_data = []
    for n in range(0, 14):
        list_of_data.append([yrs[n].text] + [state] + [pops[n].text] + [v_nums[n].text] + \
            [murd_nums[n].text] + [rape_nums[n].text] + [rob_nums[n].text] + \
            [aslt_nums[n].text] + [p_nums[n].text] + [burg_nums[n].text] + \
            [larc_nums[n].text] + [mv_nums[n].text] + [v_rts[n].text] + \
            [murd_rts[n].text] + [rape_rts[n].text] + [rob_rts[n].text] + \
            [aslt_rts[n].text] + [p_rts[n].text] + [burg_rts[n].text] + \
            [larc_rts[n].text] + [mv_rts[n].text])
    with open(csv_filename, mode='a') as states_data:
        states_writer = csv.writer(states_data, delimiter=',', quoting=csv.QUOTE_ALL)
        for i in range(0, 14):
            states_writer.writerow(list_of_data[i])
    driver.close()

def get_all_states(csv_filename):
    states = ['United States-Total', 'Alabama', 'Alaska', 'Arizona', \
             'Arkansas', 'California', 'Colorado', 'Connecticut', \
             'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', \
             'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', \
             'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', \
             'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', \
             'New Hampshire', 'New Jersey', 'New Mexico', 'New York', \
             'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', \
             'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',\
              'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', \
             'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    head = ['Year', 'State', 'Population', 'Violent Crime Total', 'Murder ' + \
            'and Nonnegligent Manslaughter', 'Rape', 'Robbery', 'Aggravated '+\
             'Assault', 'Property Crime Total', 'Burglary', 'Larceny-Theft', \
            'Motor Vehicle Theft', 'Violent Crime Rate', 'Murder and ' + \
            'Nonnegligent Manslaughter Rate', 'Rape Rate', 'Robbery Rate', \
            'Aggravated Assault Rate', 'Property Crime Rate', 'Burglary ' +\
            'Rate', 'Larceny-Theft Rate', 'Motor Vechicle Theft Rate']
    with open(csv_filename, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(head)
    for state in states:
        get_state_data(state, csv_filename)

def get_national_data(starting_years, target_dir):
    #credit for custom profile: https://selenium-python.readthedocs.io/faq.html
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList",2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", target_dir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get('https://www.ojjdp.gov/ojstatbb/ezaucr/asp/ucr_display.asp')
    for start in starting_years:
        state_object = driver.find_element_by_xpath("//option [@value=0]")
        state_object.click()
        year_object = driver.find_element_by_xpath("//input [@name='rdoYear'] \
            [@VALUE="+str(start)+"]")
        year_object.click()
        age_object = driver.find_element_by_xpath("//input [\
            @name='rdoData'] [@VALUE='1c']")
        age_object.click()
        update_object = driver.find_element_by_xpath("//button \
            [@name='submit'] [@value='Update Table']")
        update_object.click()
        data_object = \
            driver.find_element_by_xpath("//a [@title='Download CSV file']")
        data_object.click()
    driver.close()

def get_city_data(city_state, csv_filename):
    city_agencies = {'Colorado Springs, CO': 'Colorado Springs', \
                    'Washington, DC': 'Washington Metropolitan Police Dept', \
                    'Jacksonville, FL': 'Jacksonville', 'Lexington, KY': \
                    'Lexington-Fayette County Police Department', 'Baltimore, MD': \
                    'Baltimore City Police Dept', 'Las Vegas, NV': 'Las '+\
                    'Vegas Metropolitan Police Department', 'Charlotte, NC': \
                    'Charlotte-Mecklenburg Police Department', \
                    'Cleveland, OH': 'Cleveland', 'Pittsburgh, PA': \
                    'Pittsburgh', 'Nashville, TN': 'Nashville-Davidson Metro'+\
                    ' Police Dept', 'Fort Worth, TX': 'City of Fort Worth '+\
                    'Police Dept', 'Laredo, TX': 'Laredo'}
    state_keys = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': \
                 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': \
                 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': \
                 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', \
                 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': \
                 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': \
                 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': \
                 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': \
                 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': \
                 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', \
                 'NY': 'New York', 'NC': 'North Carolina', 'ND': \
                 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': \
                 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': \
                 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', \
                 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': \
                 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': \
                 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'}
    sep = city_state.split(',')
    city = sep[0]
    state_key = sep[1].strip()
    state = state_keys[state_key]
    print(city_state)
    if city_state not in city_agencies.keys():
        agency = city + ' Police Dept'
    else:
        agency = city_agencies[city_state]
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)
    driver.get('https://www.ucrdatatool.gov/Search/Crime/Local/JurisbyJuris.cfm')
    c = "[contains(text(), '" + state + "')]"
    state_obj = driver.find_elements_by_xpath("//select[@name='StateId']/*"+c)\
                [0]
    state_obj.click()
    all_pops = driver.find_elements_by_xpath("//select"+\
               "[@name='BJSPopulationGroupId']/*[contains(text(), 'All')]")[0]
    all_pops.click()
    for val in range(2, 5):
        string = str(val)
        pop_object = driver.find_elements_by_xpath("//select"+\
               "[@name='BJSPopulationGroupId']/option[@value="+string+"]")[0]
        pop_object.click()
    next_page = driver.find_elements_by_xpath("//input[@name='NextPage'"+\
                    " and @type='submit']")[0]
    next_page.click()
    if driver.find_elements_by_xpath("//*[@class='acsCloseButton acsAbandonButton ']") != []:
        x_button = driver.find_elements_by_xpath("//*[@class='acsCloseButton acsAbandonButton ']")[0]
        print(x_button)
        x_button.click()
    c_2 = "[contains(text(), '" + agency + "')]"
    agency_obj = driver.find_elements_by_xpath("//select[@name="+\
                "'CrimeCrossId']/*"+c_2)[0]
    agency_obj.click()
    for choice in range(1, 5):
        string = str(choice)
        data_object = driver.find_elements_by_xpath("//select[@name="+\
                        "'DataType']/option[@value= "+string+"]")[0]
        data_object.click()
    year_start = driver.find_elements_by_xpath("//select[@name='YearStart']"+\
                "/option[@value='2001']")[0]
    year_start.click()
    year_end = driver.find_elements_by_xpath("//select[@name='YearEnd']"+\
                "/option[@value='2014']")[0]
    year_end.click()
    next_next_pg = driver.find_elements_by_xpath("//input[@name='NextPage'"+\
                " and @type='submit']")[0]
    next_next_pg.click()
    if driver.find_elements_by_xpath("//*[@class='acsCloseButton acsAbandonButton ']") != []:
        x_button = driver.find_elements_by_xpath("//*[@class='acsCloseButton acsAbandonButton ']")[0]
        x_button.click()
    yrs = driver.find_elements_by_xpath("//td[@headers='year']")
    pops = driver.find_elements_by_xpath("//td[@headers='population']")
    v_nums = driver.find_elements_by_xpath("//td[@headers="+\
                  "'num vcrime1 vctot']")
    murd_nums = driver.find_elements_by_xpath("//td[@headers="+\
                 "'num vcrime1 murd']")
    rape_nums = driver.find_elements_by_xpath("//td[@headers="+\
                      "'num vcrime1 rape']")
    rob_nums = driver.find_elements_by_xpath("//td[@headers="+\
                   "'num vcrime1 rob']")
    aslt_nums = driver.find_elements_by_xpath("//td[@headers="+\
                        "'num vcrime1 aggr']")
    p_nums = driver.find_elements_by_xpath("//td[@headers="+\
                          "'num pcrime1 pctot']")
    burg_nums = driver.find_elements_by_xpath("//td[@headers="+\
                    "'num pcrime1 burg']")
    larc_nums = driver.find_elements_by_xpath("//td[@headers="+\
                   "'num pcrime1 larc']")
    mv_nums = driver.find_elements_by_xpath("//td[@headers="+\
                    "'num pcrime1 mvtheft']")
    v_rts = driver.find_elements_by_xpath("//td[@headers="+\
                   "'rate vcrime2 vctot2']")
    murd_rts = driver.find_elements_by_xpath("//td[@headers="+\
                  "'rate vcrime2 murd2']")
    rape_rts = driver.find_elements_by_xpath("//td[@headers="+\
                       "'rate vcrime2 rape2']")
    rob_rts = driver.find_elements_by_xpath("//td[@headers="+\
                    "'rate vcrime2 rob2']")
    aslt_rts = driver.find_elements_by_xpath("//td[@headers="+\
                         "'rate vcrime2 aggr2']")
    p_rts = driver.find_elements_by_xpath("//td[@headers="+\
                    "'rate pcrime2 pctot2']")
    burg_rts = driver.find_elements_by_xpath("//td[@headers="+\
                     "'rate pcrime2 burg2']")
    larc_rts = driver.find_elements_by_xpath("//td[@headers="+\
                    "'rate pcrime2 larc2']")
    mv_rts = driver.find_elements_by_xpath("//td[@headers="+\
                     "'rate pcrime2 mvtheft2']")
    list_of_data = []
    for n in range(0, 14):
        list_of_data.append([yrs[n].text] + [city_state] + \
            [pops[n].text] + [v_nums[n].text] + [murd_nums[n].text] + \
            [rape_nums[n].text] + [rob_nums[n].text] + [aslt_nums[n].text] + \
            [p_nums[n].text] + [burg_nums[n].text] + [larc_nums[n].text] + \
            [mv_nums[n].text] + [v_rts[n].text] + [murd_rts[n].text] + \
            [rape_rts[n].text] + [rob_rts[n].text] + [aslt_rts[n].text] + \
            [p_rts[n].text] + [burg_rts[n].text] + [larc_rts[n].text] + \
            [mv_rts[n].text])
    with open(csv_filename, mode='a') as cities_data:
        cities_writer = csv.writer(cities_data, delimiter=',', quoting=csv.QUOTE_ALL)
        for i in range(0, 14):
            cities_writer.writerow(list_of_data[i])
    driver.close()

def get_all_cities(csv_filename):
    cities = ['Anchorage, AK', 'Mobile, AL', 'Chandler, AZ', 'Mesa, AZ', \
             'Anaheim, CA', 'Bakersfield, CA', 'Chula Vista, CA', 'Long ' +\
             'Beach, CA', 'Oakland, CA', 'Riverside, CA', 'Sacramento, CA', \
             'Santa Ana, CA', 'Stockton, CA', 'Aurora, CO', 'Colorado ' +\
             'Springs, CO', 'Miami, FL', 'Orlando, FL', 'Tampa, FL', \
             'Atlanta, GA', 'Fort Wayne, IN', 'Wichita, KS', 'Louisville, KY',\
              'New Orleans, LA', 'Minneapolis, MN', 'St. Paul, MN', \
             'St. Louis, MO', 'Greensboro, NC', 'Raleigh, NC', \
             'Lincoln, NE', 'Omaha, NE', 'Jersey City, NJ', 'Newark, NJ', \
             'Henderson, NV', 'Buffalo, NY', 'Cincinnati, OH', 'Cleveland, '+\
              'OH', 'Toledo, OH', 'Tulsa, OK', 'Pittsburgh, PA', 'Arlington' +\
             ', TX', 'Corpus Christi, TX', 'Laredo, TX', 'Plano, TX', \
             'Virginia Beach, VA', 'Tuscon, AZ', 'Fresno, CA', 'San ' +\
             'Francisco, CA', 'Denver, CO', 'Washington, DC', 'Jacksonville' +\
             ', FL', 'Honolulu, HI', 'Indianapolis, IN', 'Louisville, KY', \
             'Boston, MA', 'Baltimore, MD', 'Detroit, MI', 'Charlotte, NC', \
             'Albuquerque, NM', 'Columbus, OH', 'Oklahoma City, OK', \
             'Portland, OR', 'Memphis, TN', 'Nashville, TN', 'Austin, TX', \
             'Fort Worth, TX', 'El Paso, TX', 'Seattle, WA', 'Milwaukee, WI', \
             'Phoenix, AZ', 'Los Angeles, CA', 'San Diego, CA', 'San Jose, ' +\
             'CA', 'Chicago, IL', 'Las Vegas, NV', 'New York City, NY', \
             'Philadelphia, PA', 'Dallas, TX', 'Houston, TX', 'San Antonio,' +\
             ' TX']
    head = ['Year', 'City', 'Population', 'Violent Crime'+\
            ' Total', 'Murder and Nonnegligent Manslaughter', 'Rape', \
            'Robbery', 'Aggravated Assault', 'Property Crime Total', \
            'Burglary', 'Larceny-Theft', 'Motor Vehicle Theft', 'Violent ' +\
            'Crime Rate', 'Murder and Nonnegligent Manslaughter Rate', \
            'Rape Rate', 'Robbery Rate', 'Aggravated Assault Rate', \
            'Property Crime Rate', 'Burglary Rate', 'Larceny-Theft Rate', \
            'Motor Vechicle Theft Rate']
    with open(csv_filename, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(head)
    for city in cities:
        get_city_data(city, csv_filename)
>>>>>>> 7b9e0d195eba18a6d2b1645b908b5ba66930ff22
