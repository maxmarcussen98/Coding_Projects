### Getting data from BJS for crimebusters ###
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

def get_national_data(csv_filename):
    '''
    '''
    head = ['Year', 'City', 'Population', 'Violent Crime'+\
            ' Total', 'Murder and Nonnegligent Manslaughter', 'Rape', \
            'Robbery', 'Aggravated Assault', 'Property Crime Total', \
            'Burglary', 'Larceny-Theft', 'Motor Vehicle Theft']

    with open(csv_filename, mode='a') as national_data:
        national_writer = csv.writer(national_data, delimiter=',', quoting=csv.QUOTE_ALL)
        national_writer.writerow(head)

    driver = webdriver.Firefox()
    driver.get('https://www.bjs.gov/index.cfm?ty=datool&surl=/arrests/index.cfm#')
    driver.find_elements_by_xpath("//*[@title='National Estimates']")[0].click()
    #alpha = driver.find_elements_by_xpath("//script[@language='javascript']")[2].click()
    driver.find_elements_by_xpath("//a[@id='atab1']")[0].click()
    driver.find_elements_by_xpath("//option[@value=1]")[0].click()

    
    grab_from_site = ['Violent Crime Index', 'Murder and Non-Negligent' +\
    ' Manslaughter', 'Forcible Rape', 'Robbery', 'Aggravated Assault', 'Property' +\
    ' Crime Index', 'Larceny-Theft', 'Motor Vehicle Theft']
    #for year in range(1980, 2015):
    year = 1980
    data_list = [str(year), 'United States-Total', 'N/A']
    driver.find_elements_by_xpath("//option[@value="+str(year)+"]")[0].click()
    driver.find_elements_by_xpath("//a[@title='Generate Results']")[0].click()
    alpha = driver.find_elements_by_xpath("//th")
    print(alpha[0].text)


get_national_data('asdf.csv')