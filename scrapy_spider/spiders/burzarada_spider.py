import scrapy
from scrapy_spider.items import JobsItem

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
        # print(response.body.decode('utf-8'))

        # html_file = open('index.html', 'w', encoding="utf-8")
        # html_file.write(response.body.decode('utf-8'))
        # html_file.close()

        # Set the viewport to 75
        
        # if response.css('select#ctl00_MainContent_ddlPageSize > option[selected="selected"]::attr(value)').extract() != 75:
        # href = response.xpath('//select[@id="ctl00_MainContent_ddlPageSize"]/@onchange').extract()
        href = response.xpath('//select[@id="ctl00_MainContent_ddlPageSize"]').extract()
        print(href)
        # eventTarget = href.replace("javascript:setTimeout('__doPostBack(\'", "").replace("\',\'\')', 0)", "")
        eventTarget = "ctl00$MainContent$ddlPageSize"
        # print(eventTarget)
        eventArgument = response.css('#__EVENTARGUMENT::attr(value)').extract()
        lastFocus = response.css('#__LASTFOCUS::attr(value)').extract()
        viewState = response.css('#__VIEWSTATE::attr(value)').extract()
        viewStateGenerator = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract()
        viewStateEncrypted = response.css('#__VIEWSTATEENCRYPTED::attr(value)').extract()
        pageSize = '75'
        sort = '0'

        yield scrapy.FormRequest( 

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

            callback=self.parse_multiple_pages 
            
        )
        # else:
        print("Viewport Set to 75!")

        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        # for tag in response.css('select#tag > option ::attr(value)').extract(): 
        #     yield scrapy.FormRequest.from_response( response, formdata={'tag': tag}, callback=self.parse_results, )
    
    def parse_multiple_pages(self, response):
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("Multiple Page Dealers")
        # print(response.body.decode('utf-8'))
        # See how many pages to open in viewport 75

        pages = response.xpath('//*[@id="ctl00_MainContent_gwSearch"]//tr[last()]//li')
        # pages = response.xpath('/html/body/form/section/div/div/div[1]/div[3]/div/div[2]/table/tbody/tr[76]/td/div/div/ul/li[2]/a').extract()

        print("////////////////////////////////////////////")
        print("length of pages: ", len(pages))
        print("////////////////////////////////////////////")

        if len(pages) != 0:   
            for page in pages:

                href = page.xpath('/@href').extract()

                eventTarget = href.replace("javascript:__doPostBack('", "").replace("','')", "")
                eventArgument = response.css('#__EVENTARGUMENT::attr(value)').extract()
                lastFocus = response.css('#__LASTFOCUS::attr(value)').extract()
                viewState = response.css('#__VIEWSTATE::attr(value)').extract()
                viewStateGenerator = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract()
                viewStateEncrypted = response.css('#__VIEWSTATEENCRYPTED::attr(value)').extract()
                pageSize = '75'
                sort = '0'

                print(eventTarget)

                yield scrapy.FormRequest( 

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

                    callback=self.parse_links 
                    
                )
        
        else:
            # self.parse_links(response)
            links = response.xpath('//a[@class="TitleLink"]/@href').extract()
            print("////////////////////////////////////////////")
            print("length of links: ", len(links))
            print("////////////////////////////////////////////")

            for link in links:
                link = 'https://burzarada.hzz.hr/' + link
                print(link)
                yield scrapy.Request(url=link, callback=self.parse_job)

    def parse_links(self, response):
        links = response.xpath('//a[@class="TitleLink"]/@href').extract()
        print("////////////////////////////////////////////")
        print("length of links: ", len(links))
        print("////////////////////////////////////////////")

        for link in links:
            link = 'https://burzarada.hzz.hr/' + link
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_job)

    def parse_job(self, response):

        item = JobsItem()

        print(response.body.decode('utf-8'))
        
        html_file = open('index.html', 'w', encoding="utf-8")
        html_file.write(response.body.decode('utf-8'))
        html_file.close()
        
        url = response.request.url,
        print("url: ", url)

        title = response.xpath('//*[@id="ctl00_MainContent_pnlAjaxBlock"]/ajaxblock/div/div/h3/font/font').get(),
        print("title: ", title)
        
        if "/Details/" in response.request.url:
            source = "Mojposao",
        else:
            source = "Poslovac"
        print("source: ", source)

        employer = response.xpath('//*[@id="ctl00_MainContent_lblNazivPoslodavca"]/font/font/text()').get(),
        print('employer: ', employer)

        workplace = response.xpath('//*[@id="ctl00_MainContent_lblMjestoRada"]/font/font').get(),
        print('workplace: ', workplace)

        start_date = response.xpath('//*[@id="ctl00_MainContent_lblVrijediOd"]/text()').get(),
        print('start_date: ', start_date)

        end_date = response.xpath('//*[@id="ctl00_MainContent_lblVrijediDo"]/text()').get(),
        print('end_date: ', end_date)

        description1 = ' '.join(response.xpath('//*[@id="ctl00_MainContent_lblSmjestaj"]/font/font/text()').getall()),
        print('end_date: ', end_date)

        description2 = ' '.join(response.xpath('//*[@id="ctl00_MainContent_lblNaknada"]/font/font/text()').getall()),

        requirements = ' '.join(response.xpath('//*[@id="ctl00_MainContent_bulRazinaObrazovanja"]/li[1]/font/font/*/text()').getall()),

        benefits = ' '.join(response.xpath('//*[@id="ctl00_MainContent_bulRazinaObrazovanja"]/li[1]/font/font/*/text()').getall()),

        category = ' '.join(response.xpath('//*[@id="ctl00_MainContent_lblVrstaZaposlenja"]/font/text()').getall()),

        item["url"] = url
        item["title"] = title
        item["source"] = source
        item["employer"] = employer
        item["workplace"] = workplace
        item["start_date"] = start_date
        item["end_date"] = end_date
        item["category"] = category
        item["description1"] = description1
        item["description2"] = description2
        item["requirements"] = requirements
        item["benefits"] = benefits

        print(item)

        yield item
    
    # def parse_results(self, response): 
    #     for quote in response.css("div.quote"): 
    #         yield { 'quote': quote.css('span.content ::text').extract_first(), 'author': quote.css('span.author ::text').extract_first(), 'tag': quote.css('span.tag ::text').extract_first(), }
