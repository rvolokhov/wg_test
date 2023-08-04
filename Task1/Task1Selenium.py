import pytest
import pytest_check as check
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re

# setup chrome
chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chr_options)
# go to page
driver.get("https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites")
# retrieve data from 2nd column
column_popularity = driver.find_elements(By.XPATH,
                                         "//caption[contains(text(),'Programming languages used in most popular websites')]/..//tbody/tr/td[2]")
# retrieve data from 1st column
column_website = driver.find_elements(By.XPATH,
                                      "//caption[contains(text(),'Programming languages used in most popular websites')]/..//tbody/tr/td[1]")
# retrieve data from 3rd column
column_frontend = driver.find_elements(By.XPATH,
                                       "//caption[contains(text(),'Programming languages used in most popular websites')]/..//tbody/tr/td[3]")
# retrieve data from 4th column
column_backend = driver.find_elements(By.XPATH,
                                      "//caption[contains(text(),'Programming languages used in most popular websites')]/..//tbody/tr/td[4]")


# put all data we've retrieved to appropriate lists (except 'popularity' column)
websites = []
for data in column_website:
    websites.append(re.sub(r'\[\d+\]', '', data.text))
frontends = []
for data in column_frontend:
    frontends.append(re.sub(r'\[\d+\]', '', data.text))
backends = []
for data in column_backend:
    backends.append(re.sub(r'\[\d+\]', '', data.text))

popularities = []
# get numbers from popularity column and put them to the list
for item in column_popularity:
    a = item.text
    a = re.sub(r'[.,]', '', a)
    a = re.findall(r'\d+', a)[0]
    popularities.append(int(a))
driver.close()

# create list of tuples consisting of info we've got
wikidata = []
for x in range(len(popularities)):
    wikidata.append((websites[x], popularities[x], frontends[x], backends[x]))

# testdata we need to compare with
testdatavalues = [10 ** 7, int(1.5 * 10 ** 7), 5 * 10 ** 7, 10 ** 8, 5 * 10 ** 8, 10 ** 9, int(1.5 * 10 ** 9)]


@pytest.mark.parametrize("testdatavalue", testdatavalues)
def test_multiplication(testdatavalue):
    for wikivalue in wikidata:
        check.less(wikivalue[1], testdatavalue,
                   "\n" + wikivalue[0] + "(Frontend:" + wikivalue[2] + " \ Backend:" + wikivalue[3] + ") has " +
                   str(wikivalue[1]) + " unique visitors per month. (expected more then " + str(testdatavalue) + ")")
