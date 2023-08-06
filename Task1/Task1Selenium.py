import pytest
import pytest_check as check
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
from WikiData import WikiData

driver: webdriver = None
# testdata we need to compare with
testdata_values = [10 ** 7, int(1.5 * 10 ** 7), 5 * 10 ** 7, 10 ** 8, 5 * 10 ** 8, 10 ** 9, int(1.5 * 10 ** 9)]
# list of tuples consisting of info we've got
wikidata = []
url_wiki = "https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites"


def setup_browser():
    global driver
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chr_options)


def goto_url(url: str):
    global driver
    driver.get(url)


@pytest.fixture(scope="session", autouse=True)
def precondition(request):
    global driver
    setup_browser()
    goto_url(url_wiki)
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

    # put all data we've retrieved to appropriate lists
    websites = []
    # pattern to parse digits along with '[]'
    pattern = r'\[\d+\]'
    for data in column_website:
        websites.append(re.sub(pattern, "", data.text))
    frontends = []
    for data in column_frontend:
        frontends.append(re.sub(pattern, "", data.text))
    backends = []
    for data in column_backend:
        backends.append(re.sub(pattern, "", data.text))

    popularity = []
    # parse numbers from popularity column and put them to the list
    for item in column_popularity:
        a = item.text
        # remove '.' and ',' symbols from number
        a = re.sub(r'[.,]', "", a)
        # get number
        a = re.findall(r'\d+', a)[0]
        popularity.append(int(a))

    # create list of tuples consisting of info we've got
    for i in range(0, len(websites)):
        wikidata.append(WikiData(website=websites[i], popularity=popularity[i], frontend=frontends[i], backend=backends[i]))

    # will be called after the last test finished
    request.addfinalizer(finalizer)


def finalizer():
    global driver
    driver.close()


@pytest.mark.parametrize("testdata_value", testdata_values)
def test_comparing(testdata_value):
    for i in range(0, len(wikidata)):
        check.less(wikidata[i].popularity, testdata_value,
                   "\n" + wikidata[i].website + "(Frontend:" + wikidata[i].frontend + " \ Backend:" + wikidata[i].backend + ") has " + str(wikidata[i].popularity) + " unique visitors per month. (expected more then " + str(testdata_value) + ")")
