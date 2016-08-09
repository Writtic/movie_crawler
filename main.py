#!/usr/bin/python
#-*- coding: utf-8 -*-
import unittest
import time
# PySpark
import sys
from webCrawler import Crawling
class TestSuite(unittest.TestCase):
    def test(self):
        crawling = Crawling()
        print("Welcome to JobJang Crawler!")
        user_id = input("오픈한글 아이디를 입력해주세요 : ")
        user_pw = input("오픈한글 비밀번호를 입력해주세요 : ")
        #getContent는 getMovies에서 받아온 url에 따라 영화의 [타이틀, 평점, 평론]을 긁는다.
        results = crawling.getContent(crawling.getMovies(), user_id, user_pw)
        print("success!")
        #time.sleep(5)

def main():
    unittest.main()
    unittest.close()

if __name__ == "__main__":
    main()
