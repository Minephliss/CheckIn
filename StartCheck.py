#coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
import time
import yagmail

def className(classname):
    if classname == '电气20201班': return True
    elif classname == '电气20202班': return True
    elif classname == '电气20203班': return True
    elif classname == '电气20204班': return True
    elif classname == '电信20201班': return True
    elif classname == '电信20202班': return True
    elif classname == '电信20203班': return True
    elif classname == '电信20204班': return True
    elif classname == '电气20181班': return True
    elif classname == '机械类20213班': return True
    else: return False

def pageCount(driver: WebDriver):
    pagecount = driver.find_element(By.ID, 'app-pagination').find_elements(By.TAG_NAME, 'li')[1].text
    lst = pagecount.split(' ')

    print("\rProgress:{:.2f}%".format((float(lst[0]) / float(lst[2])) * 100), end='')

    if lst[0] == lst[2]:
        return False
    else:
        return True

chrome_options = Options()
chrome_options.add_argument('--headless')
wd = webdriver.Chrome(r'/home/cust/workstation/Chrome/chromedriver', options=chrome_options)
wd.implicitly_wait(2)

wd.get('http://zhxg.shzu.edu.cn/gbi/app/4fdf48dc797943b7bf9c207fb7bf6fce.ghtml?_hd=no&appback=yes')
time.sleep(2)

#重设日期
wd.find_element(By.CLASS_NAME, 'ui-nowrap').click()
time.sleep(0.3)

wd.find_element(By.ID, 'btn-query-reset').click()
time.sleep(0.3)

wd.find_element(By.CLASS_NAME, 'input-group').click()
time.sleep(0.3)

wd.find_element(By.CLASS_NAME, 'date_btn_box').find_element(By.CLASS_NAME, 'lcalendar_finish').click()
time.sleep(0.3)

wd.find_element(By.ID, 'btn-query-submit').click()
time.sleep(0.3)

print('Time Set Complete')

res_list = []

while pageCount(wd):
    print('hello')
    try:
        tex = wd.find_elements(By.TAG_NAME, 'tbody')[1].text.find('机械')
    except:
        time.sleep(0.5)
        tex = wd.find_elements(By.TAG_NAME, 'tbody')[1].text.find('机械')

    if tex != -1:
        time.sleep(1)

        #获取表格中每一行的元素，与该表格中一共行元素
        sheet = wd.find_elements(By.TAG_NAME, 'tbody')[1]
        datas = sheet.find_elements(By.TAG_NAME, 'tr')
        capacity = len(datas)

        #遍历每一行
        for row in range(1, capacity):
            class_name = datas[row].find_element(By.ID, str(row) + '_2').text
            stud_name = datas[row].find_element(By.ID, str(row) + '_4').text
            if className(class_name):
                res_list.append(class_name + ' ' + stud_name)
            
        wd.find_element(By.CLASS_NAME, 'icon-right').click()
        time.sleep(0.25)
    else:
        wd.find_element(By.CLASS_NAME, 'icon-right').click()
        time.sleep(0.25)


yag = yagmail.SMTP(user="endermanem@qq.com",host="smtp.qq.com",password='psxissuhtktgeaef')

if len(res_list):
    yag.send(to='endermanemail@gmail.com', subject='List of Students', contents=res_list)
    print(res_list)
else:
    yag.send(to='endermanemail@gmail.com', subject='List of Students', contents='All students has done!')

wd.quit()
