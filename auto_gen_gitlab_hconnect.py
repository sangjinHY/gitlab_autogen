
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import xlrd
import time

## This is auto generater for gitlab group & a lots of repository
## we need
##      "chromedriver"
##      "'xls' file that name of 'group_name' valuable""
##      ""'xls' file fill that student id number"



####common value
group_create = 1 # is group already create? yes = 0 or create new group = 1
year = "2018"
lecture_code = "test"
class_code = "0000"
username = "1111"
password = "2222"
driver_path = "/Users/sangjin/Downloads/chromedriver"
####

#### You have to set those variables below
####group
group_desc = "2018 Object Oriented Programming"
group_visibility_level=1 # 1=Private, 2=Internal, 3=Public
####

####repository
project_desc = "test reopository"
number_of_student = 1
####

group_name = year + "_" + lecture_code + "_" + class_code
project_name_prefix = year + "_" + lecture_code + "_"

#### login
driver = webdriver.Chrome(driver_path)
driver.implicitly_wait(3)
driver.get('https://hconnect.hanyang.ac.kr')
driver.find_element_by_name('user[login]').send_keys(username)
driver.find_element_by_name('user[password]').send_keys(password)


## create group
if group_create == 1:
    # click login button
    driver.find_element_by_xpath('//*[@id="new_user"]/div[4]/input').click()

    ##### make group
    # enter the group category
    driver.get('https://hconnect.hanyang.ac.kr/dashboard/groups')

    #click new group button
    driver.find_element_by_xpath('//*[@id="content-body"]/div/div/a').click()

    # input group name
    driver.find_element_by_xpath('//*[@id="group_path"]').send_keys(group_name)

    # input group description
    driver.find_element_by_xpath('//*[@id="group_description"]').send_keys(group_desc)

    # click group visibility level
    if group_visibility_level == 1 :
        driver.find_element_by_xpath('//*[@id="group_visibility_level_0"]').click()
    elif group_visibility_level == 2 :
        driver.find_element_by_xpath('//*[@id="group_visibility_level_10"]').click()
    elif group_visibility_level == 3 :
        driver.find_element_by_xpath('//*[@id="group_visibility_level_20"]').click()

    driver.find_element_by_xpath('//*[@id="new_group"]/div[6]/input').click()


## create student repository
for i in range(0,number_of_student):
	wb = xlrd.open_workbook(group_name+'.xls')
	sheet = wb.sheet_by_index(0)

	student_id = str(int(sheet.cell(i, 0).value))
	
	# click left-top menu button
	driver.find_element_by_xpath('/html/body/header/div/div/button[1]/i').click()

	time.sleep(1)

	# click left-top menu button - Groups
	driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[3]/a').click()

	time.sleep(1)

	# click class group
	driver.find_element_by_xpath('//a[@href="/'+group_name+'"]').click()

# ------------------------------ Original Routine ------------------------------
	# click New Project button
	driver.find_element_by_xpath('//*[@id="content-body"]/div[2]/div[1]/div/a').click()

	# input project name
	driver.find_element_by_xpath('//*[@id="project_path"]').send_keys(project_name_prefix + student_id)

	# input project description
	driver.find_element_by_xpath('//*[@id="project_description"]').send_keys(project_desc)
	
	# click Create project button
	driver.find_element_by_xpath('//*[@id="new_project"]/input[3]').click()

# ---------------------------- Project page ----------------------------
	# click project setting button
	driver.find_element_by_xpath('//*[@id="project-settings-button"]/i[1]').click()

	# click project member setting button
	driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div/ul/li[1]/a').click()

# -------------------------------- Project setting page --------------------------------
	# click project setting button
	# input student id to invite
	driver.find_element_by_xpath('//*[@id="s2id_autogen2"]').send_keys(student_id)

	# delay 1 sec
	#driver.implicitly_wait(3)
	time.sleep(1)

	if driver.find_element_by_xpath('//*[@id="select2-drop"]/ul/li').get_attribute('class') == 'select2-no-results':
		print("failed - no account: " + student_id)
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		continue
	time.sleep(1)

	# select student
	driver.find_element_by_xpath('//*[@id="select2-drop"]').click()

	# set permissions to Developer
	driver.find_element_by_xpath('//*[@id="access_level"]').send_keys('Developer')

	# click Add to project button
	driver.find_element_by_xpath('//*[@id="new_project_member"]/input[3]').click()

	print("success to create project: " + student_id)

# click left-top menu button - Groups
driver.find_element_by_xpath('/html/body/header/div/div/h1/span/a').click()
