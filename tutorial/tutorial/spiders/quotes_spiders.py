import scrapy
from scrapy_splash import SplashRequest
#from loginform import fill_login_form

#import requests
#url = "https://github.com/login"
#r = requests.get(url)
#fill_login_form(url, r.text, "john", "secret")
#(,
#  ('login', 'john'),
#  ('password', 'secret')],
# u'https://github.com/session',
 #'POST')

class loginSpider(scrapy.Spider):
    name = "login"
    login_page = 'http://172.31.4.49/login'
    interface = 'http://172.31.4.49/'

    #authentication
    def start_requests(self):
        return [scrapy.http.FormRequest(url=self.login_page,
                                 formdata = {'user_name': 'admin', 'user_password': 'admin'},
                                 callback=self.check_login,
                                 args={'wait': 5}
                                    )]

    def check_login(self, response):
        if "logout" in response.body:
            self.login
        else:
            print("Login failed")
            print response.body

    #def login(self, response):
#        return SplashRequest(url=self.interface,
#                             endpoint='render.html',
#                             args={'wait': 10}
#                             )

    def parse(self, response):
        print response.body


#class QuotesSpider(scrapy.Spider):
 #   name = "quotes"
#
#    def start_requests(self):
#        urls = [
#            'http://quotes.toscrape.com/page/1/',
#            'http://quotes.toscrape.com/page/2/',
#        ]
#        for url in urls:
#            yield scrapy.Request(url=url, callback=self.parse)
#
##        page = response.url.split("/")[-2]
#        filename = 'quotes-%s.html' % page
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#        self.log('Saved file %s' % filename)
#

