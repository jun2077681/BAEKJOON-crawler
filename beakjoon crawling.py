# -*- coding:utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
print(current_dir)

#input user id and pw
user_id = input('user_id : ')
user_pw = input('user_pw : ')

#chrome driver location (same as code)
driver = webdriver.Chrome('chromedriver.exe')
driver.implicitly_wait(1)

#beakjoon login page
driver.get('https://www.acmicpc.net/login')

driver.find_element_by_name('login_user_id').send_keys(user_id)
driver.find_element_by_name('login_password').send_keys(user_pw)

driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/form/div[4]/div[2]/button').click()

if driver.current_url!='https://www.acmicpc.net/':
    print('ID or PW error.')
    exit(-1)

#get problem number in beakjoon user page
driver.get('https://www.acmicpc.net/user/'+user_id)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

problem_numbers = list(map(lambda x:x.text, soup.findAll("span", {"class":"problem_number"})))

#extension dictionary
extension = {'C':'.c', 'C++14':'.cpp', 'C++':'.cpp', 'Java':'.java', 'Python 2':'.py', 'Python 3':'.py', 'Text':'.txt', 'Assembly (32bit)':'.asm'}

for num in problem_numbers:
    #get successed sources page
    driver.get('https://www.acmicpc.net/status/?problem_id=' + num + '&user_id=' + user_id + '&language_id=-1&result_id=4&from_mine=1')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    trs = soup.find(id="status-table").tbody.find_all('tr')

    filenum = 0

    for tr in trs:
        #get source info
        td = tr.find_all('td')
        language = td[6].find_all('a')[0].text.replace('\n','').replace('\t','')
        source_num = td[0].text

        #get code
        driver.get('https://www.acmicpc.net/source/'+source_num)
        code_page = BeautifulSoup(driver.page_source, 'html.parser')
        code_line = code_page.find_all("pre", {'class','CodeMirror-line'})
        code = ''
        
        for i in code_line:
            #delete zero width space
            if i.text.encode('utf-8').hex() == 'e2808b':
                code = code + '\n'
                continue
            code = code + i.text + '\n'

        #save path
        directory = current_dir+'/baekjoon/source/'+num
        
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except:
            print("Directory Error.")
            exit(-1)

        while True:
            if os.path.exists(directory+'/'+file_name):
                filenum = filenum+1
            else:
                break

        file_name = num+'_'+str(filenum)+extension[language]
            
        f = open(directory+'/'+file_name, 'w', encoding='UTF-8')
        f.write(code)
        f.close()
