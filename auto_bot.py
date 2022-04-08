from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

import os, sys,csv
import pandas as pd
import numpy as np
weblink = 'http://www.nepalstock.com/stocklive'

option = Options()
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})
# option.add_argument('--disable-gpu')
# option.add_argument('--headless')
# option.add_argument('start-maximized')
# option.add_argument('--log-level 3') 
# option.add_argument('headless')
# option.add_argument('window-size=1200x600')

class jordan():
    def __init__(self,data_list = [],num_rows=0):
        self.driver = webdriver.Chrome(options=option)
        self.data_list  = data_list
        self.num_rows = num_rows

    def data_printer(self):
        self.num_rows = (len(self.driver.find_elements_by_class_name('alnright'))/6)-1
        temp = []

        for i in range(3,int(self.num_rows)+3):
            Company  = self.company
            Date = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[2]'%(i)).text
            Transactions = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[3]'%(i)).text
            TotalSharesTraded = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[4]'%(i)).text
            TotalAmount = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[5]'%(i)).text
            MaxPrice = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[6]'%(i)).text
            MinPrice = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[7]'%(i)).text
            ClosePrice = self.driver.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[%d]/td[8]'%(i)).text
            
            temp = [Company,Date,Transactions,TotalSharesTraded,TotalAmount,MaxPrice,MinPrice,ClosePrice]
            self.data_list.append(temp)

        print('data printed for page ')
        return self


    def csv_writer(self,company):
        output_filename = 'Share_Data_'+ company +'.csv'
        row_header =['Company','Date','Transactions','TotalSharesTraded','TotalAmount','MaxPrice','MinPrice','ClosePrice'] 
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
        # list_of_companies = self.driver.find_element_by_id('stock-symbol')
        # self.available_stocks = [x.text for x in list_of_companies.find_elements_by_tag_name('option')][1:]

        selector = self.driver.find_element_by_xpath('//*[@id="nav"]/li[2]/a')
        selector.click()
        day_90clicker = self.driver.find_element_by_xpath('//*[@id="nav"]/li[2]/ul/li[4]/a')
        day_90clicker.click()

        #90days page entered
        start_date = self.driver.find_element_by_id('startDateStockWise')
        start_date.click()
        dateentry1 = self.driver.find_element_by_xpath('/html/body/div[6]/div[1]/table/thead/tr[1]/th[2]')
        dateentry1.click()

        year_switch = self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/table/thead/tr/th[2]')
        year_switch.click()
        year_switch2 = self.driver.find_element_by_xpath('/html/body/div[6]/div[3]/table/thead/tr/th[1]')
        year_switch2.click()
        year = self.driver.find_element_by_xpath('/html/body/div[6]/div[3]/table/tbody/tr/td/span[2]')
        year.click()
        month1 =  self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/table/tbody/tr/td/span[1]')
        month1.click()
        day = self.driver.find_element_by_xpath('/html/body/div[6]/div[1]/table/tbody/tr[1]/td[6]')
        day.click()

        end_date = self.driver.find_element_by_id('endDateStockWise')
        end_date.click()
        dateentry1 = self.driver.find_element_by_xpath('/html/body/div[7]/div[1]/table/tbody/tr[3]/td[6]')
        dateentry1.click()

        random_nepse_issue = self.driver.find_element_by_xpath('//*[@id="home-contents"]/table/tbody/tr[1]/td/label')
        random_nepse_issue.click()

        seletion = self.driver.find_element_by_xpath('//*[@id="stockwiseprice"]/label[4]/select/option[5]')
        seletion.click()

        # stock_selector = self.driver.find_element_by_xpath('//*[@id="stock-symbol"]')
        # stock_selectors = stock_selector.click()

        # stock = self.driver.find_element_by_id('stock-symbol')
        # stock.click()
        list_of_companies = self.driver.find_element_by_id('stock-symbol')
        stocks = [x.text for x in list_of_companies.find_elements_by_tag_name('option')][1:]

        #### Need to enter a loop here for all of the companies later
        # for i in range(2,401):
        for i in range(11,401):        
            stock = self.driver.find_element_by_xpath('//*[@id="stock-symbol"]/option[%d]'%i)
            stock.click()
            self.company = stocks[i-2]
            print('Data scrap running :'+ self.company)
            filter_button = self.driver.find_element_by_id('stocksubmit')
            filter_button.click()

        # firstpage_rownum = (len(self.driver.find_element_by_class_name('alnright'))/6)-1
            # if self.company not in ('ADBL', 'AHPC', 'AKJCL', 'AKPL', 'ALBSL', 'ALICL', 'API', 'BARUN', 'BBC', 'BFC', 'BNT', 'BOKL', 'BPCL', 'CBBL', 'CBL', 'CCBL', 'CFCL', 'CHCL', 'CHL', 'CIT', 'CLBSL', 'CMF1', 'CORBL', 'CZBIL', 'DDBL', 'DHPL', 'EBL', 'EDBL', 'EIC', 'FMDBL', 'FOWAD', 'GBBL', 'GBIME', 'GBLBS', 'GFCL', 'GGBSL', 'GHL', 'GILB', 'GIMES1', 'GLBSL', 'GLICL', 'GMFBS', 'GMFIL', 'GRDBL', 'GUFL', 'HBL', 'HDHPC', 'HDL', 'HGI', 'HIDCL', 'HPPL', 'HURJA', 'ICFC', 'IGI', 'ILBS', 'JBBL', 'JFL', 'JOSHI', 'JSLBB', 'KBL', 'KKHC', 'KMCDB', 'KPCL', 'KRBL', 'KSBBL', 'LBBL', 'LBL', 'LEMF', 'LGIL', 'LICN', 'LLBS', 'LVF1', 'MBL', 'MDB', 'MEGA', 'MERO', 'MFIL', 'MLBBL', 'MLBL', 'MNBBL', 'MPFL', 'MSMBS', 'NABIL', 'NADEP', 'NBB', 'NBF2', 'NBL', 'NCCB', 'NEF', 'NFS', 'NGPL', 'NHDL', 'NHPC', 'NIB', 'NIBLPF', 'NIBSF1', 'NICA', 'NICGF', 'NICL', 'NIL', 'NLBBL', 'NLG', 'NLIC', 'NLICL', 'NMB', 'NMBHF1', 'NMBMF', 'NMFBS', 'NSEWA', 'NTC', 'NUBL', 'OHL', 'PCBL', 'PFL', 'PIC', 'PICL', 'PLIC', 'PMHPL', 'PPCL', 'PRIN', 'PROFL', 'PRVU', 'RADHI', 'RBCL', 'RHPC', 'RHPL', 'RLFL', 'RMDC', 'RRHP', 'RSDC', 'SABSL', 'SADBL', 'SAEF', 'SANIMA', 'SAPDBL', 'SBI', 'SBL', 'SCB', 'SDESI', 'SEF', 'SFCL', 'SHINE', 'SHIVM', 'SHL', 'SHPC', 'SIC', 'SICL', 'SIFC', 'SIL', 'SINDU', 'SJCL', 'SKBBL', 'SLBBL', 'SLBSL', 'SLICL', 'SMATA', 'SMB', 'SMFBS', 'SPARS', 'SPDL', 'SRBL', 'STC', 'TMDBL', 'TRH', 'UFL', 'UIC', 'UMHL', 'UNHPL', 'UNL', 'UPCL', 'UPPER', 'VLBS'):
            # if self.company not in ( 'BARUN', 'BBC', 'BFC', 'BNT', 'BOKL', 'BPCL', 'CBBL', 'CBL', 'CCBL', 'CFCL', 'CHCL', 'CHL', 'CIT', 'CLBSL', 'CMF1', 'CORBL', 'CZBIL', 'DDBL', 'DHPL', 'EBL', 'EDBL', 'EIC', 'FMDBL', 'FOWAD', 'GBBL', 'GBIME', 'GBLBS', 'GFCL', 'GGBSL', 'GHL', 'GILB', 'GIMES1', 'GLBSL', 'GLICL', 'GMFBS', 'GMFIL', 'GRDBL', 'GUFL', 'HBL', 'HDHPC', 'HDL', 'HGI', 'HIDCL', 'HPPL', 'HURJA', 'ICFC', 'IGI', 'ILBS', 'JBBL', 'JFL', 'JOSHI', 'JSLBB', 'KBL', 'KKHC', 'KMCDB', 'KPCL', 'KRBL', 'KSBBL', 'LBBL', 'LBL', 'LEMF', 'LGIL', 'LICN', 'LLBS', 'LVF1', 'MBL', 'MDB', 'MEGA', 'MERO', 'MFIL', 'MLBBL', 'MLBL', 'MNBBL', 'MPFL', 'MSMBS', 'NABIL', 'NADEP', 'NBB', 'NBF2', 'NBL', 'NCCB', 'NEF', 'NFS', 'NGPL', 'NHDL', 'NHPC', 'NIB', 'NIBLPF', 'NIBSF1', 'NICA', 'NICGF', 'NICL', 'NIL', 'NLBBL', 'NLG', 'NLIC', 'NLICL', 'NMB', 'NMBHF1', 'NMBMF', 'NMFBS', 'NSEWA', 'NTC', 'NUBL', 'OHL', 'PCBL', 'PFL', 'PIC', 'PICL', 'PLIC', 'PMHPL', 'PPCL', 'PRIN', 'PROFL', 'PRVU', 'RADHI', 'RBCL', 'RHPC', 'RHPL', 'RLFL', 'RMDC', 'RRHP', 'RSDC', 'SABSL', 'SADBL', 'SAEF', 'SANIMA', 'SAPDBL', 'SBI', 'SBL', 'SCB', 'SDESI', 'SEF', 'SFCL', 'SHINE', 'SHIVM', 'SHL', 'SHPC', 'SIC', 'SICL', 'SIFC', 'SIL', 'SINDU', 'SJCL', 'SKBBL', 'SLBBL', 'SLBSL', 'SLICL', 'SMATA', 'SMB', 'SMFBS', 'SPARS', 'SPDL', 'SRBL', 'STC', 'TMDBL', 'TRH', 'UFL', 'UIC', 'UMHL', 'UNHPL', 'UNL', 'UPCL', 'UPPER', 'VLBS'):
            if self.company not in ('NBL', 'NCCB', 'NEF', 'NFS', 'NGPL', 'NHDL', 'NHPC', 'NIB', 'NIBLPF', 'NIBSF1', 'NICA', 'NICGF', 'NICL', 'NIL', 'NLBBL', 'NLG', 'NLIC', 'NLICL', 'NMB', 'NMBHF1', 'NMBMF', 'NMFBS', 'NSEWA', 'NTC', 'NUBL', 'OHL', 'PCBL', 'PFL', 'PIC', 'PICL', 'PLIC', 'PMHPL', 'PPCL', 'PRIN', 'PROFL', 'PRVU', 'RADHI', 'RBCL', 'RHPC', 'RHPL', 'RLFL', 'RMDC', 'RRHP', 'RSDC', 'SABSL', 'SADBL', 'SAEF', 'SANIMA', 'SAPDBL', 'SBI', 'SBL', 'SCB', 'SDESI', 'SEF', 'SFCL', 'SHINE', 'SHIVM', 'SHL', 'SHPC', 'SIC', 'SICL', 'SIFC', 'SIL', 'SINDU', 'SJCL', 'SKBBL', 'SLBBL', 'SLBSL', 'SLICL', 'SMATA', 'SMB', 'SMFBS', 'SPARS', 'SPDL', 'SRBL', 'STC', 'TMDBL', 'TRH', 'UFL', 'UIC', 'UMHL', 'UNHPL', 'UNL', 'UPCL', 'UPPER', 'VLBS'):
                
                continue
            temp = ((self.driver.find_element_by_class_name('pager')).text)[-1]
            num_of_pages = int(temp)
        # print(num_of_pages)

            for i in range(num_of_pages):
                self.data_printer()
                print('Data printed for %d page'%(i+1))
                if i != num_of_pages-1:
                    self.goto_next_page(i)

                elif i == num_of_pages-1:
                    self.csv_writer(self.company)
                    self.data_list.clear()
                    first_page_link =self.driver.find_element_by_partial_link_text('1') 
                    first_page_link.click()

        self.driver.close()
        
        return self.data_list
        

        
x = jordan()
x.link_initiator()

