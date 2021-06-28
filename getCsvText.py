# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import lxml
import csv
import itertools
import re

#
LOGIN_ID = ''
LOGIN_PASS = ''

SELLERURL = ''
LISTURL = SELLERURL + ''
PRODUCTURL = SELLERURL + ''

LOGINURL = ''

PRODUCTCODE_PRE_BUYA = ''
PRODUCTSUPPLIERCODE = ''
PRODUCTCODE = ''

# open csv create product list
BUYALIST = ''
PRODUCTLIST_CSV = []

ORIGINAL_CSV = ''

# prepare csv header
CSVHEADERLIST = []
csvHeaderFile = open('', 'r', encoding='cp932', errors='ignore', newline='')
csvHeader = csv.reader(csvHeaderFile, doublequote=True, quotechar='"', skipinitialspace=True)

# driver Firefox
FIREFOXDRIVER = ''
driver = webdriver.Firefox(executable_path=FIREFOXDRIVER)
driver.implicitly_wait(3)
driver.get(LOGINURL)

# site login
driver.find_element_by_name('loginEmail').send_keys(LOGIN_ID)
driver.find_element_by_name('loginPassword').send_keys(LOGIN_PASS)
driver.find_element_by_name('login').click()

# create csv header
for data in csvHeader:
    CSVHEADERLIST = data

# create product list
PRODUCTCATEGORY = []
PRODUCTLIST = []
with open(BUYALIST, 'r', errors='ignore', newline='') as f:
    reader = csv.reader(f, delimiter=',', doublequote=True, quotechar='"', skipinitialspace=True)
    for row in reader:
        PRODUCTCATEGORY.append(row[0])
        PRODUCTLIST.append(row[1:])

# append csv header csv content
csvContent = [CSVHEADERLIST]

# product code prefix
PRODUCTCODEPREFIX = ''

#
for i, rowByCategory in enumerate(PRODUCTLIST):

    prodCat = PRODUCTCATEGORY[i]

    for id in rowByCategory:

        # create URL
        targetURL = PRODUCTURL + str(id)
        targetPage = driver.get(targetURL)
        targetContent = driver.page_source
        targetSoup = BeautifulSoup(targetContent, 'lxml')

        #
        content = ''
        priceContent = ''

        path = prodCat
        name = ''
        codePref = PRODUCTCODEPREFIX + str(id)
        price = ''
        headline = ''
        caption = ''
        explanation = ''

        costPrice = ''

        dummy = ''

        # content
        if targetSoup.select_one(''):
            content = targetSoup.select_one('')
        else:
            print(id + ' :no [secondary]')

        # get name
        if content.select_one('') is not None:
            name = content.select_one('').text.lstrip().rstrip()
        else:
            print(id + ' :no [name]')

        # get headline
        if content.select_one('') is not None:
            headline = content.select_one('').text.lstrip().rstrip()
        else:
            print(id + ' :no [headline]')

        # get caption
        if content.select_one('') is not None:
            caption = content.select_one('').text.lstrip().rstrip()
        else:
            print(id + ' :no [caption]')

        # get explanation
        if content.select_one('') is not None:
            explanation = content.select_one('').text.lstrip().rstrip()
        else:
            print(id + ' :no [explanation]')

        # main image
        contentMain = ''
        mainImageTag = ''
        target = ''

        if targetSoup.select_one('') is not None:
            contentMain = targetSoup.select_one('')
            mainImageTag = contentMain.select_one('')
            if mainImageTag is not None:

                # TODO delete if no problem
                # if mainImageTag.get('src').endswith('jpg') or mainImageTag.get('src').endswith('gif') or mainImageTag.get('src').endswith('png'):
                target = mainImageTag.get('src')

                # check url schema
                if not target.startswith('//'):

                    ext = target.split('/')[-1].split('.')[-1]

                    # check extension
                    if re.fullmatch(r'jpg|jpeg|gif|png', ext, re.IGNORECASE) is not None:
                        res = requests.get(target)

                        if res.ok:
                            with open('' + PRODUCTCODE + '-' + PRODUCTSUPPLIERCODE + '-' + id + '.' + ext, 'wb') as f:
                                f.write(res.content)

        # check main image
        if target is '' or None:
            print(id + ' :no [**Main Image**]')

        # sub image
        # sub image srcs
        subImageSrcs = []
        subImageContent = ''
        subImageContentTags = ''

        if targetSoup.select_one('') is not None:
            subImageContent = targetSoup.select_one('')

            subImageContentTags = subImageContent.find_all('img')

            for imgTag in subImageContentTags:
                # TODO delete if no problem
                # if imgTag.get('src').endswith('.jpg') or imgTag.get('src').endswith('.gif') or imgTag.get('src').endswith('.png'):
                subImageSrcs.append(imgTag.get('src'))

        if targetSoup.select_one('') is not None:
            subImageContent = targetSoup.select_one('')

            subImageContentTags = subImageContent.find_all('img')

            for imgTag in subImageContentTags:
                # TODO delete if no problem
                # if imgTag.get('src').endswith('.jpg') or imgTag.get('src').endswith('.gif') or imgTag.get('src').endswith('.png'):
                subImageSrcs.append(imgTag.get('src'))

        for i, target in enumerate(subImageSrcs, 1):
            if not target.startswith('//'):
                ext = target.split('/')[-1].split('.')[-1]

                # check extension
                if re.fullmatch(r'jpg|jpeg|gif|png', ext, re.IGNORECASE) is not None:
                    res = requests.get(target)

                    print('res.statuscode:', res.status_code)

                    if res.ok:
                        postfix = str(i)

                        subFileName = PRODUCTCODE + '_' + PRODUCTCODE + '-' + PRODUCTSUPPLIERCODE + '-' + id + '_' + postfix

                        with open('' + subFileName, 'wb') as f:
                            if len(res.content) == 0:
                                print('sub image res content 0: ', id)
                            f.write(res.content)

                        imgPath = ''
                        addImageTag = '\r\n<div style="width: 600px; margin: auto;"><img src="' + imgPath + subFileName + '" /></div>\r\n'
                        caption += addImageTag

        # price content
        if targetSoup.select_one('.p-product-set') is not None:
            priceContent = targetSoup.select_one('.p-product-set')
        else:
            print('priceContent', id)

        # jan under price content
        if priceContent.find_all('', class_='') is not None:
            itemrow = priceContent.find_all('', class_='')

            for counter, itemData in enumerate(itemrow, 1):
                optionName = ''
                stockNumber = ''
                jan = ''
                jodai = ''
                costPrice = ''
                code = codePref + '-' + str(counter)
                taxtype2 = ''

                # assign code to image file name

                # get optionName
                if itemData.select_one('.__name') is not None:
                    optionName = itemData.select_one('.__name').text.lstrip().rstrip()
                else:
                    print(id + ' :no [optionName]')

                # get stockNumber
                if itemData.select_one('.__no') is not None:
                    stockNumber = itemData.select_one('.__no').text.lstrip('\r\n').rstrip('\r\n')
                    stockNumber = stockNumber.replace('品番', '')
                else:
                    print(id + ' :no [stockNumber]')

                # get jan
                if itemData.select_one('.__jan') is not None:
                    jan = itemData.select_one('.__jan').text.lstrip('\r\n').rstrip('\r\n')
                    jan = jan.replace('JANコード', '')
                    jan = jan.replace('JAN', '')
                else:
                    print(id + ' :no [jan]')

                # jodai
                if itemData.select_one('.__jodai') is not None:
                    jodai = itemData.select_one('.__jodai').text.lstrip('\r\n').rstrip('\r\n')
                else:
                    print(id + ' :no [jodai]')

                # tax option
                if itemData.select_one('.c-tax-type-2'):
                    taxtype2 = itemData.select_one('.c-tax-type-2').text.lstrip().rstrip('\r\n')
                else:
                    print(id + ': no [taxtype2]')

                # cost price
                if itemData.select_one('.__tax-price') is not None:
                    costPrice = itemData.select_one('.__tax-price').text.lstrip().rstrip()
                    costPrice = costPrice.replace(',', '')
                    costPrice = costPrice.replace('円', '')
                else:
                    print(id + ' :no [costPrice]')

                # itemrow == 1 append list
                csvContent.append([path, name, code, dummy, dummy, price, dummy, dummy, headline, caption, dummy, explanation, dummy, dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,jan,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,costPrice,optionName,stockNumber,jodai,taxtype2])

            else:
                print(id, 'multiple price-set')

def main():
    # open and auto close csv, make one if not exists
    with open(ORIGINAL_CSV, 'w', encoding='cp932', newline='', errors='ignore') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')

        # output
        if csvContent is not None:
            try:
                writer.writerows(csvContent)
                print('ORIGINAL_CSV successfully saved')
            except:
                print('something wrong occurred')
        else:
            print('error occurred')

    # close browser
    driver.close()

#
if __name__ == '__main__':
    main()
