import scrapy 

class JobSpider(scrapy.Spider): 
    
    # def __init__(self):
    #     self.html_file

    name = 'burzarada' 
    start_urls = ['https://burzarada.hzz.hr/Posloprimac_RadnaMjesta.aspx'] 
    download_delay = 1.5 

    def parse(self, response): 
        i = 0
        for href in response.css('div.NKZbox > div.KategorijeBox > a ::attr(href)').extract(): 
            i = i + 1
            if i > 1:
                break
            print("i = ", i)

            # Getting form data
            eventTarget = href.replace("javascript:__doPostBack('", "").replace("','')", "")
            eventArgument = response.css('#__EVENTARGUMENT::attr(value)').extract()
            lastFocus = response.css('#__LASTFOCUS::attr(value)').extract()
            viewState = response.css('#__VIEWSTATE::attr(value)').extract()
            viewStateGenerator = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract()
            viewStateEncrypted = response.css('#__VIEWSTATEENCRYPTED::attr(value)').extract()
            
            print("eventTarget:", eventTarget)

            # path_to_html = eventTarget + '.html'

            # self.html_file = open(path_to_html, 'w')

            yield scrapy.FormRequest( 

                'https://burzarada.hzz.hr/Posloprimac_RadnaMjesta.aspx', 

                formdata = { 
                    '__EVENTTARGET': eventTarget, 
                    '__EVENTARGUMENT': eventArgument, 
                    '__LASTFOCUS': lastFocus, 
                    '__VIEWSTATE': viewState, 
                    '__VIEWSTATEGENERATOR': viewStateGenerator,
                    '__VIEWSTATEENCRYPTED': viewStateEncrypted,
                },

                callback=self.parse_category 
            
            ) 
            
    # def parse_category(self, response): 
    #     for tag in response.css('select#tag > option ::attr(value)').extract(): 
    #         yield scrapy.FormRequest( 'http://quotes.toscrape.com/filter.aspx', formdata={ 'author': response.css( 'select#author > option[selected] ::attr(value)' ).extract_first(), 'tag': tag, '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first() }, callback=self.parse_results, )
            
    def parse_category(self, response): 
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("Response")
        # print(response)
        print(response.body.decode('utf-8'))

        # html_file = open('index.html', 'w', encoding="utf-8")
        # html_file.write(response.body.decode('utf-8'))
        # html_file.close()

        # Set the viewport to 75
        
        # if response.css('select#ctl00_MainContent_ddlPageSize > option[selected="selected"]::attr(value)').extract() != 75:
        # href = response.xpath('//select[@id="ctl00_MainContent_ddlPageSize"]/@onchange').extract()
        href = response.xpath('//select[@id="ctl00_MainContent_ddlPageSize"]').extract()
        print(href)
        eventTarget = href.replace("javascript:setTimeout('__doPostBack(\'", "").replace("\',\'\')', 0)", "")
        print(eventTarget)
        eventArgument = response.css('#__EVENTARGUMENT::attr(value)').extract()
        lastFocus = response.css('#__LASTFOCUS::attr(value)').extract()
        viewState = response.css('#__VIEWSTATE::attr(value)').extract()
        viewStateGenerator = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract()
        viewStateEncrypted = response.css('#__VIEWSTATEENCRYPTED::attr(value)').extract()
        pageSize = 75
        sort = 0

        scrapy.FormRequest( 

            'https://burzarada.hzz.hr/Posloprimac_RadnaMjesta.aspx', 

            formdata = { 
                '__EVENTTARGET': eventTarget, 
                '__EVENTARGUMENT': eventArgument, 
                '__LASTFOCUS': lastFocus, 
                '__VIEWSTATE': viewState, 
                '__VIEWSTATEGENERATOR': viewStateGenerator,
                '__VIEWSTATEENCRYPTED': viewStateEncrypted,
                'ctl00$MainContent$ddlPageSize': pageSize,
                'ctl00$MainContent$ddlSort': sort,
            },

            callback=self.parse_category 
            
        )
        # else:
        print("Viewport Set to 75!")


        # See if there are multiple pages

        # print(response.css('.prInfobox > a ::attr(href)').extract())
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        # for tag in response.css('select#tag > option ::attr(value)').extract(): 
        #     yield scrapy.FormRequest.from_response( response, formdata={'tag': tag}, callback=self.parse_results, )
    
    def parse_results(self, response): 
        for quote in response.css("div.quote"): 
            yield { 'quote': quote.css('span.content ::text').extract_first(), 'author': quote.css('span.author ::text').extract_first(), 'tag': quote.css('span.tag ::text').extract_first(), }
