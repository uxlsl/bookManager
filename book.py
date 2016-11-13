# -*- coding:utf-8 -*-

from urllib import urlencode
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

brower = webdriver.Chrome()
brower.set_page_load_timeout(10)


def get_book_classs(bookname):
    try:
        brower.get('http://search.jd.com/Search?' + urlencode({'keyword':bookname, 'enc':'utf-8', 'pvid':'qeg4hgvi.ttuz7i'}))
    except TimeoutException:
        pass
    try:
        e = brower.find_element_by_css_selector('#J_goodsList > ul > li:nth-child(1) > div > div.p-name > a')
        book_home = e.get_attribute('href')
        d = pq(url=book_home)
        a = d('#root-nav > div > div > span:nth-child(2) > a')
        return [i.encode('utf-8') for i in a.contents()]
    except:
        return None


def get_book_tags(bookname):
    try:
        brower.get('https://book.douban.com/subject_search?' + urlencode({'search_text':bookname, 'cat':1001}))
    except TimeoutException:
        pass
    try:
        e = brower.find_element_by_css_selector('#content > div > div.article > ul > li:nth-child(1) > div.info > h2 > a')
        book_home = e.get_attribute('href')
        d = pq(url=book_home)
        a = d('#db-tags-section span a')
        return [i.encode('utf-8') for i in a.contents()]
    except:
        return None


def make_book():
    with open('book.list', 'r') as fi, open('out.txt','w') as fo:
        for bookname in fi:
            bookname = bookname.strip()
            if bookname:
                print bookname
                book_classs = get_book_classs(bookname) or ''
                book_tags = get_book_tags(bookname) or ''
                fo.write('{}\t{}\t{}\n'.format(bookname.strip(), '|'.join(book_classs), '|'.join(book_tags)))


def fetch_book_tags(path='out.txt'):
    with open(path, 'r') as f:
        tags = []
        for line in f:
            try:
                data = line.split()
                t = data[2]
                x = t.split('|')
                tags.extend(x)
            except IndexError:
                pass
    return tags


if __name__ == '__main__':
    make_book()
