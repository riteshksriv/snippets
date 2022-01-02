from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.support.ui import Select
import time

#url after opening a window via selenium API
url = "http://localhost:50199"
session_id = "10890368d927c544dad1e638e6d06012"

driver = webdriver.Remote(command_executor=url,desired_capabilities={})
driver.close()   # this prevents the dummy browser
driver.session_id = session_id

datas = [
  #["date", "amount"]
  #["15-Mar-2017", "123"]
  #["31-Dec-2016", "456"],
]
#driver.maximize_window()

def addData(element, data:str):
  if(element != None):
    element.clear()
    element.send_keys(data)


def select(driver, data):
  select = Select(driver.find_element_by_xpath('//*[@formcontrolname="DtlsForeignEquityDebtInterest_CountryCode"]'))
  select.select_by_value('2')
  names = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_NameOfEntity']")
  addData(names, 'Adobe Systems Inc')
  nature = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_NatureOfEntity']")
  addData(nature, 'Multi National Company')
  address = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_AddressOfEntity']")
  addData(address, '345 Park Ave, San Jose')
  zips = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_ZipCode']")
  addData(zips, '95110')

  fillDate(driver, data[0])

  #select = Select(driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_NatureOfInt']"))
  #select.select_by_value('BENIFICIARY')
  initial = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_InitialValOfInvstmnt']")
  addData(initial, data[1])
  peak = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_PeakBalanceDuringPeriod']")
  addData(peak, '0')
  close = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_ClosingBalance']")
  addData(close, '0')
  gross = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_TotGrossAmtPaidCredited']")
  addData(gross, '0')
  proceeds = driver.find_element_by_xpath("//*[@formcontrolname='DtlsForeignEquityDebtInterest_TotGrossProceeds']")
  addData(proceeds, '0')
  add = driver.find_element_by_xpath("//*[contains(@class, 'primaryButton') and contains(@class, 'largeButton') and contains(text(), 'Add')]")
  add.click()
  time.sleep(5)

def clickBDetails(driver):
  items = driver.find_elements_by_xpath("//*[contains(@class, 'rep_parent_comp')]")
  for item in items:
    if(item.text.startswith('A3. Details of Foreign Equity')):
      item.click()
      time.sleep(2)
      break

def clickAddAnother(driver):
  items = driver.find_elements_by_xpath("//*[contains(@class, 'addDetailsButton') and contains(@class,'uniservenxtcmp_button') and contains(text(), 'Add Another')]")
  for item in items:
    parent = item.find_element_by_xpath("./../../../../../../..")
    if(parent.text.startswith('A3.')):
      item.click()
      time.sleep(10)
      break

def getviaparent(driver, parentxpath, xpath):
  parent =  driver.find_element_by_xpath(parentxpath)
  item = parent.find_element_by_xpath(xpath)
  return item

def clicktime(driver:WebDriver, xpath: str, since: str, add: int):
  items = driver.find_elements_by_xpath("//*[contains(@class, '{xpath}') and not(contains(@class, '{xpath}s')) and not(contains(@class, 'old {xpath}'))]".format(xpath=xpath))
  for item in items:
    if((item.text.isdigit() and int(item.text)+add>=int(since)) or (item.text == since)):
      item.click()
      time.sleep(1)
      break

#
def fillDate(driver:WebDriver, since:str):
  parent =  driver.find_element_by_xpath("//*[contains(text(), 'Date of acquiring the interest')]")
  icons = parent.find_elements_by_xpath("//*[contains(@class, 'input-group-text') and contains(@class, 'calender-icon')]")
  for icon in icons:
    if(icon.is_displayed()):
      icon.click()
      time.sleep(1)

      button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.datepicker-days .datepicker-switch')))
      button.click()
      button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.datepicker-months .datepicker-switch')))
      button.click()
      button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.datepicker-years .datepicker-switch')))
      button.click()

      clicktime(driver, "decade", since[7:], 9)
      clicktime(driver, "year", since[7:], 0)
      clicktime(driver, "month", since[3:6], 0)
      clicktime(driver, "day", since[0:2], 0)
      break

def fillAll(driver, data):
  clickBDetails(driver)
  clickAddAnother(driver)
  select(driver, data)

#fillDate(driver, "24-Apr-2016")
for data in datas:
  fillAll(driver, data)



