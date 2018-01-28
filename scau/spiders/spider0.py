from time import sleep
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from scrapy import FormRequest, Request
from scrapy.http.cookies import CookieJar
from scrapy.spider import Spider


class Spider0(Spider):
    name = 'scau'

    def __init__(self, json):
        self.json = eval(json)

        self.url0 = 'http://202.116.160.166/default_vsso.aspx'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
        }
        self.data0 = {
            'Button1': '',
            'Textbox1': self.json['username'],
            'TextBox2': self.json['password'],
        }
        self.data1 = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '7AEF2E62',
            'zymc': '2501计算机科学与技术主修专业||2015',
            'xx': '',
            'Button5': '本专业选课'
        }
        self.data2 = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '7AEF2E62',
            'zymc': '2501计算机科学与技术主修专业||2015',
            'xx': ''
        }

    def start_requests(self):
        cookie_jar = CookieJar()
        yield FormRequest(self.url0, formdata=self.data0, headers=self.header, meta={'cookiejar': cookie_jar}, callback=self.parse)

    def parse(self, response):
        print(response.meta)
        soup = BeautifulSoup(response.body, 'lxml')
        list0 = soup.find('ul', class_='sub').find_all('a')
        cookie = response.meta['cookiejar']
        cookie.extract_cookies(response, response.request)
        url = urljoin(response.url, list0[0]['href'])
        yield Request(url=url, callback=self.parse1, meta={'cookiejar': cookie}, dont_filter=True)

    def parse1(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        self.data1['__VIEWSTATE'] = soup.find(
            'input', attrs={'name': '__VIEWSTATE'})['value']
        yield FormRequest(url=response.url, formdata=self.data1, headers=self.header, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        list0 = soup.find('table', class_='datelist').find_all('tr')[1:-1]
        self.data2['__VIEWSTATE'] = soup.find(
            'input', attrs={'name': '__VIEWSTATE'})['value']
        for l in list0:
            url = urljoin(response.url, l.find('a')['onclick'].split('\'')[1])
            yield Request(url=url, callback=self.parse3, meta={'cookiejar': response.meta['cookiejar']})
            sleep(3)
        if soup.find('tr', attrs={'nowrap': 'nowrap'}).find('a').get_text() == '2':
            self.data2['__EVENTTARGET'] = 'kcmcgrid:_ctl14:_ctl1'
            yield FormRequest(url=response.url, formdata=self.data2, headers=self.header, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse2, dont_filter=True)

    def parse3(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        data = {
            '__EVENTTARGET': 'Button1',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': 'dDwxMzg2MzMxOTMyO3Q8cDxsPHp5ZG07eHk7ZHFzemo7UkxYWjt6eW1jO3h6Yjt4bTtzZmJqa2M7Y3hibW1zMTtjeGJtbXMyO2h4d3o7PjtsPDI1MDE75pWw5a2m5LiO5L+h5oGv5a2m6ZmiOzIwMTU7MTvorqHnrpfmnLrnp5HlrabkuI7mioDmnK87MTXorqHnrpfmnLo1O+WRqOWTsuW4hjvlkKY75YWN5L+uO+mHjeS/rjtpPDE+Oz4+O2w8aTwwPjs+O2w8dDw7bDxpPDI+Oz47bDx0PHQ8OztsPGk8MT47Pj47Oz47Pj47Pj47PtZtbw44K4K+Pk/zJ3IpXzS1NKmL',
            '__VIEWSTATEGENERATOR': 'AC27D4D4',
            'xkkh': '',
            'RadioButtonList1': '0',
        }
        data['xkkh'] = soup.find(
            'input', attrs={'type': 'radio'}).get('value', None)
        if data['xkkh'] is not None:
            print(soup.find('span', id='Label1').get_text().replace('\xa0', ' '))
            yield FormRequest(response.url, formdata=data, headers=self.header, meta={'cookiejar': response.meta['cookiejar'], 'dont_redirect': True}, callback=None)
