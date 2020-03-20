from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

import os, sys,csv
import pandas as pd
import numpy as np
weblink = 'http://www.nepalstock.com/main/stockwiseprices/index/1/?startDate=2019-12-01&endDate=2020-03-05&stock-symbol=385&_limit=20'
option = Options()
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})
option.headless = True          #doesnt open any overhead windows

class jordan():
    def __init__(self,data_list = [],num_rows=0):
        self.driver = webdriver.Chrome(options=option)
        self.data_list  = data_list
        self.num_rows = num_rows
    def data_printer(self):
        self.num_rows = (len(self.driver.find_elements_by_class_name('alnright'))/6)-1
        temp = []

        for i in range(3,int(self.num_rows)+3):
            Date = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[2]'%(i)).text
            Transactions = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[3]'%(i)).text
            TotalSharesTraded = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[4]'%(i)).text
            TotalAmount = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[5]'%(i)).text
            MaxPrice = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[6]'%(i)).text
            MinPrice = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[7]'%(i)).text
            ClosePrice = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[8]'%(i)).text
            
            temp = [Date,Transactions,TotalSharesTraded,TotalAmount,MaxPrice,MinPrice,ClosePrice]
            self.data_list.append(temp)

        print('data printed for page ')
        return self


    def csv_writer(self):
        output_filename = 'Share_Data.csv'
        row_header =['Date','Transactions','TotalSharesTraded','TotalAmount','MaxPrice','MinPrice','ClosePrice'] 
        with open(output_filename,'w',newline='') as file:
            writer = csv.writer(file,delimiter = '|')       # the | is system specific for \t in my old laptop. This might have to be changed in future.
            writer.writerows([row_header])
            for rows in self.data_list:
                writer.writerows([rows])

        return  True

    def goto_next_page(self,iteration):
        if iteration ==0:
            next_page_link = self.driver.find_element_by_xpath('//*[@id="home-contents"]/table/tbody/tr[%d]/td/div/a[2]'%(self.num_rows+3))
            next_page_link.click()
        else:
            first_page_link =self.driver.find_element_by_partial_link_text('1') 
            # first_page_link = self.driver.find_element_by_xpath('//*[@id="home-contents"]/table/tbody/tr[503]/td/div/a[2]')
            first_page_link.click()
            print('First page re-reached')
            next_page_link = self.driver.find_element_by_xpath('//*[@id="home-contents"]/table/tbody/tr[%d]/td/div/a[%d]'%(self.num_rows+3,iteration+2))
            next_page_link.click()
            

        print('%d page gone'%(iteration+1))
        return self

    def link_initiator(self):
        self.driver.get(weblink)
        list_of_companies = self.driver.find_element_by_id('stock-symbol')
        stocks = [x.text for x in list_of_companies.find_elements_by_tag_name('option')][1:]

        print((stocks[-1]))
        # stock = self.driver.find_element_by_xpath('//*[@id="stock-symbol"]/option[1]')
        # print(stock.text)

        # temp = ((self.driver.find_element_by_class_name('pager')).text)[-1]
        # num_of_pages = int(temp)
        # print(num_of_pages)

        # for i in range(num_of_pages):
        #     self.data_printer()
        #     print('Data printed for %d page'%(i+1))
        #     if i != num_of_pages-1:
        #         self.goto_next_page(i)



        # # self.driver.close()
        # self.csv_writer()
        return self.data_list
        
x = jordan()
z = x.link_initiator()
