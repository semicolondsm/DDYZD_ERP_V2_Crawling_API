from .crawler import Crawler
import requests
import json
import re

class ElevenST(Crawler):
    def __init__(self, url):
        super().__init__(url)
        self.first_option_api = 'http://www.11st.co.kr/product/SellerProductDetailAjax.tmall?method=getTopOptionInfoJson&prdNo='+self.get_prd_no()
        self.sub_option_api = 'http://www.11st.co.kr/products/'+self.get_prd_no()+'/sub-options?optNoArr={}&optLvl=2&selOptCnt=3&strNo=0'
        self.last_option_api = 'http://www.11st.co.kr/products/'+self.get_prd_no()+'/last-options?optNoArr={}&selOptCnt={}&strNo=0'
        self.option_apis = [self.first_option_api, self.sub_option_api, self.last_option_api]
        
            
    def get_prd_no(self):
        p = re.compile('\/([0-9]+)\/?')
        return p.findall(self.url)[0]

    def get_prd_title(self):
        return self.soup.find('h1', class_='title').contents[0]

    def get_opt_title_list(self):
        response = requests.get(self.option_apis[0])
        response.encoding = 'UTF-18'
        response = json.loads(response.text[1:-1]) 
        return response.get('selOptTitleList')

    def get_option_json(self, num, opt_no_arr=''):
        if(num<0 or num >2):
            return ValueError("num 변수는 0, 1, 2의 숫자만 유효합니다. 현재 num값: "+str(num))
        if num == 0 or num == 1:
            url = self.option_apis[num].format(opt_no_arr)
        else:
            url = self.option_apis[num].format(opt_no_arr, len(self.get_opt_title_list()))
            print(url)

        response = requests.get(url)
        response.encoding = 'UTF-18'
        if num == 0:
            response = json.loads(response.text[1:-1])
            response = response.get('selOptList')
        else:
            response = json.loads(response.text)
            response = response.get('infoList')
        return response

    def parse_option(self, option, opt_no_arr=''):
        options = self.options
        if opt_no_arr != '':
            for opt_no in opt_no_arr.split(','):
                options = options[opt_no][1]

        options[option.get('optNo', option.get('dataOptno'))] = [{
                                'dtlOptNm': option.get('dtlOptNm', option.get('dataDtloptnm')), 
                                'stckQty': option.get('stckQty', option.get('dataStckqty')),
                                'price': option.get('price', option.get('dataPrice'))  ,
                                'minAddPrc': option.get('minAddPrc', option.get('dataMinaddprc')), 
                                'maxAddPrc': option.get('maxAddPrc', option.get('dataMaxaddprc'))
                                }, {}]
        return option.get('optNo', option.get('dataOptno'))
    
    def run(self):
        opt_list_len = len(self.get_opt_title_list())
        for sel_opt1 in self.get_option_json(num=0):
            opt_no_arr1 = self.parse_option(sel_opt1)
            if opt_list_len ==2:
                for sel_opt2 in self.get_option_json(num=2, opt_no_arr=opt_no_arr1):
                    self.parse_option(sel_opt2, opt_no_arr=opt_no_arr1)
            elif opt_list_len == 3:
                for sel_opt2 in self.get_option_json(num=1, opt_no_arr=opt_no_arr1):
                    opt_no_arr2 = opt_no_arr1+','+self.parse_option(sel_opt2, opt_no_arr=opt_no_arr1)
                    for sel_opt3 in self.get_option_json(num=2, opt_no_arr=opt_no_arr2):
                        self.parse_option(sel_opt3, opt_no_arr=opt_no_arr2)

        return self.get_opt_title_list(), self.options
