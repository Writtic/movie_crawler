#!/usr/bin/python
#-*- encoding: utf-8 -*-
import requests as rs
import bs4
import time
# csv 파일 입출력
import csv
import re
from io import StringIO
from operator import itemgetter
from datetime import datetime, date, timedelta
# 형태소 분석기
from konlpy.tag import Kkma
from konlpy.utils import pprint

class Crawling:

    def getOEval(self, text, user_id, user_pw):
    """
    오픈한글에 접속하여 감정사전에 의거한 토큰 분석을 한다.
    """
    url = "http://openhangul.com/login_ok.php"
    session = rs.session()
    login_form = {"user_id":user_id, "user_pw":user_pw}
    session.post(url, login_form)
    url = "http://openhangul.com/senti_text?q=" + text
    response = session.get(url)
    html_content = response.text.encode(response.encoding)
    navigator = bs4.BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
    #문장 전체의 긍정 부정 퍼센트 (중립, 비감성어 제외)
    content = navigator.find_all("div", {"class":"panel-body"})[3]
    pos = content.find("div", {"class":"progress-bar progress-bar-success progress-bar-striped"})['style'].replace("width: ", '').replace("%", '')
    neg = content.find("div", {"class":"progress-bar progress-bar-danger progress-bar-striped"})['style'].replace("width: ", '').replace("%", '')
    pos = float(pos)
    neg = float(neg)
    if pos and neg is not None:
        print("긍정 : %d%%, 부정 : %d%%"%(int(pos), int(neg)))
        result = [pos, neg]
    else:
        print("긍정 : %d%%, 부정 : %d%%"%(0, 0))
        result = [0, 0]
    #토큰별 긍정 부정 중립 비감성어 강도 추출
    content = navigator.find("div", {"class":"panel-body"}).tbody
    if content is not None:
        tokens = content.find_all('tr')
        for index, token in enumerate(tokens):
            if index <= len(tokens)-1:
                data1 = content.find_all('td')[index*10+1].get_text().replace("\"\r\n\t", '')
                data2 = content.find_all('td')[index*10+8].get_text().replace("\"\r\n\t", '')
                print(data1+", "+data2)

    session.close()
    return result

    def getEval(self, text, dic):
        """
        감정사전에 의거한 토큰 분석을 한다.
        """
        kkma = Kkma()
        pprint(kkma.pos(text))
        tokens = kkma.pos(text)
        score = []
        neg = 0
        neut = 0
        none = 0
        pos = 0
        for token in tokens:
            for item in dic:
                found = 0
                found = item[0].split(";")[0].count(token[0])
                if found > 0:
                    found = 0
                    found = item[0].split(";")[0].count(token[1])
                    if found > 0:
                        # max property값과 각각의 속성값을 곱해 가중치를 조절한다.
                        neg += float(item[3]) * float(item[8])
                        neut += float(item[4]) * float(item[8])
                        none += float(item[5]) * float(item[8])
                        pos += float(item[6]) * float(item[8])
                        break
        total = neg + neut + none + pos
        if total == 0:
            total = 1
        score.append(pos / total)
        score.append(neg / total)
        print("긍정 :" + score[0] + ", 부정 :" + score[1])
        return score
        # SEED tag

    def getText(self, text):
        """
        누리꾼들의 댓글은 대개 맞춤법을 준수하지 않는 경우가 다반사다.
        효과적인 분석을 위해 최대한 맞춤법을 맞춰 저장하고자 네이버 맞춤법 검사기에
        140자평을 쿼리해 올바른 문장을 추출한다.
        """
        url = "https://m.search.naver.com/p/csearch/dcontent/spellchecker.nhn?_callback=window.__jindo2_callback._spellingCheck_0&q=" + text

        response = rs.get(url)

        temp = response.text.encode('utf-8').decode('utf-8', 'replace')
        index = temp.find("html")
        temp = temp[index + 7:-7]

        temp = temp.replace("<span class=\'re_green\'>", '')
        temp = temp.replace("<span class=\'re_purple\'>", '')
        temp = temp.replace("<span class=\'re_red\'>", '')
        temp = temp.replace("</span>", '')

        return temp.encode('utf-8').decode('utf-8', 'replace')

    def getTitle(self, url):
        """
        어떤 영화의 평가인지 인지하기 위해 영화 제목을 긁어온다.
        이는 네이버 영화 페이지가 프레임별로 분리되어 있어서
        평점란에서 영화 제목을 받아오지 못해 만든 함수이다.
        """
        response = rs.get(url)
        html_content = response.text.encode(response.encoding)
        navigator = bs4.BeautifulSoup(
            html_content, 'html.parser', from_encoding='utf-8')
        title = navigator.find("div", {"class": "mv_info"})
        title = title.find('h3').a.get_text().replace("상영중\"\r\n\t", '')
        return title

    def getPage(self, url):
        """
        상영작의 평점이 5개 이상인 URL은 별도의 페이지로 나누어 표현되는데,
        이를 인식하고 페이지를 카운트하여 반환한다.
        class="score_total"
        """
        # 코드 및 관람객 리플 url(네이버는 영화별 코드를 부여해 구분함)
        # 코드 예시 : http://movie.naver.com/movie/bi/mi/point.nhn?code=122489 정글북
        url = "http://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=" + \
              self.getCode(url) + "&type=after&page=1"
        response = rs.get(url)
        html_content = response.text.encode(response.encoding)
        navigator = bs4.BeautifulSoup(
            html_content, 'html.parser', from_encoding='utf-8')
        pages = navigator.find("div", {"class": "score_total"})
        if pages is not None:
            str_num = pages.find_all('em')
            str_num = str_num[1].get_text().replace(",", "")
            num = int(str_num) / 5
            return 1 + int(num)
        return 1

    def getCode(self, url):
        """
        코드 및 관람객 리플 url(네이버는 영화별 코드를 부여해 구분함)
        코드 예시 : http://movie.naver.com/movie/bi/mi/point.nhn?code=122489 정글북
        """
        code_index = url.find("code=")
        code = url[code_index + 5:]
        return code

    def getContent(self, list, user_id, user_pw):
        """
        BS4로 추출된 영화 URL에서 내용물을 뽑아내고, csv파일로 저장한다.
        반환형 :
        list : url_lists
        result : 결과값
        """
        result = False
        count = 0
        cookie = None
        results = []
        # 감정 사전 로드
        with open("polarity.txt", "r") as polarity:
            dic = []
            cr = csv.reader(polarity)
            for row in cr:
                dic.append(row)
        # 영화 평점 및 코멘트 저장 공간 로드
        with open("result.csv", "w") as csv_file:
            cw = csv.writer(csv_file, delimiter='|')
            cw.writerow(["title", "rate", "text", "pos", "neg"])
            for index, movie_url in enumerate(list):
                # 영화 제목
                title = self.getTitle(movie_url)
                # 영화당 평점 페이지 갯수
                pages = self.getPage(movie_url)
                # 페이지별 모든 평가를 긁음
                print("영화 %s는 총 %d개의 평가페이지가 존재합니다." % (title, pages))
                for page in range(pages):
                    reply_urls = "http://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=" + \
                                 self.getCode(movie_url) + \
                        "&type=after&page=" + str(page + 1)
                    print("영화 %s의 평가 페이지 %d번째" % (title, page + 1))
                    response = rs.get(reply_urls.encode('utf-8'))
                    html_content = response.text.encode(response.encoding)
                    navigator = bs4.BeautifulSoup(
                        html_content, 'html.parser', from_encoding='utf-8')
                    # 평가 및 코멘트 추출 준비
                    content = navigator.find("div", {"class": "score_result"})
                    # 페이지가 존재할 경우 추출
                    if content is not None:
                        # 평점
                        rates = content.find_all(
                            "div", {"class": "star_score"})
                        for rate in rates:
                            rate = rate.em.get_text().replace("\"\r\n\t", '')
                            results.append([title, rate])
                        # 코멘트
                        texts = content.find_all(
                            "div", {"class": "score_reple"})
                        for text in texts:
                            text = text.p.get_text().replace("BEST", '').replace(
                                "관람객", '').replace("\"\r\n\t", '')
                            results[count].append(self.getText(text))
                            resultText = '[%d번째 평가] 영화 : %s 평점 : %s, 내용 : %s' %\
                                (count + 1, results[count][0],
                                 results[count][1], results[count][2])
                            print(resultText)
                            results[
                                count] += self.getEval(results[count][2], dic)
                            cw.writerow(results[count])
                            # 주소 및 갯수 카운터 +1
                            count += 1
                            # if count >= 39:
                            #    return results

        return results

    def getMovies(self):
        """
        BS4, request를 활용하여 URL별 존재하는 상영중인 영화
        주소를 리스팅한다.
        """
        # 네이버 현재 상영작 주소
        naver_url = "http://movie.naver.com/movie/running/current.nhn"
        # 요청
        response = rs.get(naver_url)
        # 응답으로 부터 HTML 추출
        html_content = response.text.encode(response.encoding)
        # HTML 파싱
        navigator = bs4.BeautifulSoup(
            html_content, 'html.parser', from_encoding='utf-8')
        # 네비게이터를 이용해 원하는 링크 리스트 가져오기
        # 상영작예매순위
        topMovies = navigator.find("ul", {"class": "top_thumb_lst"})
        # 상영작이 존재하는지 확인하고 각각 상영작들의 주소를 추출
        if topMovies is not None:
            topMovie = topMovies.find_all("li")
            resultList = [item.a for item in topMovie]

        # 링크 추출(각각 상영작 메인 페이지)
        url_lists = ["http://movie.naver.com" + item['href']
                     for item in resultList]

        # URL 출력
        for index, url_list in enumerate(url_lists):
            resultText = '[%d개] %s' % (index + 1, url_list)
            print(resultText)
        return url_lists
