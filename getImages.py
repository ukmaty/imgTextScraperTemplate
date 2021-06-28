# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import lxml
import csv
import itertools

# information
SELLERURL = ''
LISTURL = SELLERURL + ''
PRODUCTURL = SELLERURL + ''

PRODUCTCODE_PREFIX = ''
PRODUCTSUPPLIERCODE = ''

# open csv create product list
SELLERLIST = ''
PRODUCTLIST = []
with open(SELLERLIST, 'r', errors='ignore', newline='') as f:
    reader = csv.reader(f, delimiter=',', doublequote=True,
                        quotechar='"', skipinitialspace=True)
    for row in reader:
        PRODUCTLIST.append(row[1:])

#
imageSrcs = {}
imageTags = []

# main images srcs
mainImageSrcs = []

# content top image srcs
contentTopImageSrcs = []

# content bottom image srcs
contentBottomImageSrcs = []

# sub image srcs
subImageSrcs = []


# create image dir
def createImageDir(dirname):
    os.makedirs(dirname, exist_ok=True)

# get main images
def getMainImageSrcs():
    for rowByCategory in PRODUCTLIST:

        for id in rowByCategory:

            #
            targetURL = PRODUCTURL + str(id)
            targetHTML = requests.get(targetURL)
            targetSoup = BeautifulSoup(targetHTML.content, 'lxml')

            #
            contentMain = ''
            mainImageTag = ''
            mainImageTags = []

            # primary
            if targetSoup.select_one('') is not None:
                contentMain = targetSoup.select_one('')
                mainImageTag = contentMain.select_one('')
                mainImageTags.append(mainImageTag)

                for mainImage in mainImageTags:
                    if mainImage.get('src').endswith('jpg'):
                        mainImageSrcs.append(mainImage.get('src'))
                    elif mainImage.get('src').endswith('gif'):
                        mainImageSrcs.append(mainImage.get('src'))
                    elif mainImage.get('src').endswith('png'):
                        mainImageSrcs.append(mainImage.get('src'))

# sub image

def getSubImageSrcs():
    for rowByCategory in PRODUCTLIST:

        for id in rowByCategory:
            #
            targetURL = PRODUCTURL + str(id)
            targetHTML = requests.get(targetURL)
            targetSoup = BeautifulSoup(targetHTML.content, 'lxml')

            # content top
            contentTop = ''
            contentTopImgTags = ''

            if targetSoup.select_one('') is not None:
                contentTop = targetSoup.select_one('')

                if contentTop.find_all('img') is not None:
                    contentTopImgTags = contentTop.find_all('img')

                    for imgTag in contentTopImgTags:
                        if imgTag.get('src').endswith('.jpg'):
                            subImageSrcs.append(imgTag.get('src'))
                        elif imgTag.get('src').endswith('.gif'):
                            subImageSrcs.append(imgTag.get('src'))
                        elif imgTag.get('src').endswith('.png'):
                            subImageSrcs.append(imgTag.get('src'))

            # content bottom
            contentBottom = ''
            contentBottomImgTags = ''

            if targetSoup.select_one('') is not None:
                contentBottom = targetSoup.select_one('')

                if contentBottom.find_all('img') is not None:
                    contentBottomImgTags = contentBottom.find_all('img')

                    for imgTag in contentBottomImgTags:
                        if imgTag.get('src').endswith('.jpg'):
                            subImageSrcs.append(imgTag.get('src'))
                        elif imgTag.get('src').endswith('.gif'):
                            subImageSrcs.append(imgTag.get('src'))
                        elif imgTag.get('src').endswith('.png'):
                            subImageSrcs.append(imgTag.get('src'))

# download main images
def saveMainImages(imgsrcs):
    for i, target in enumerate(imgsrcs):
        # response for image uri
        re = requests.get(target)
        ext = target.split('/')[-1].split('.')[-1]
        productId = list(itertools.chain.from_iterable(PRODUCTLIST))[i]

        """
        # uncomment when separate images in each dirs with each names

        createImageDir('' + productId)
        save in each BUYA prductId dir
        with open('' + productId + '/' + PRODUCTCODE + '-' + PRODUCTSUPPLIERCODE + '-' + productId + '.' + ext, 'wb') as f:
            f.write(re.content)
        """

        with open('' + PRODUCTCODE_PREFIX + '-' + PRODUCTSUPPLIERCODE + '-' + productId + '.' + ext, 'wb') as f:
            f.write(re.content)

#
def saveSubImages(imgsrcs):
    productIds = list(itertools.chain.from_iterable(PRODUCTLIST))

    for productId in productIds:

        for i, target in enumerate(imgsrcs, 1):
            re = requests.get(target)
            ext = target.split('/')[-1].split('.')[-1]
            postfix = str(i)

            with open('' + PRODUCTCODE_PREFIX + '-' + PRODUCTSUPPLIERCODE + '-' + productId + '_' + postfix + '.' + ext, 'wb') as f:
                f.write(re.content)

# main
def main():
    # # create mainImageSrcs
    getMainImageSrcs()

    # # create main image dir
    createImageDir('')

    # # save main images
    saveMainImages(mainImageSrcs)

    # create subImageSrcs
    getSubImageSrcs()

    # create sub image dir
    createImageDir('')

    # save sub images
    print(subImageSrcs)
    # saveSubImages(subImageSrcs)

if __name__ == '__main__':
    main()
