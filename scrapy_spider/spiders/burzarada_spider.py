import scrapy
from scrapy_spider.items import JobsItem


class JobSpider(scrapy.Spider): 
    
    name = 'burzarada' 
    start_urls = ['https://burzarada.hzz.hr/Posloprimac_RadnaMjesta.aspx'] 
    download_delay = 1.5 

    def parse(self, response): 
        i = 0
        for href in response.css('div.NKZbox > div.KategorijeBox > a ::attr(href)').extract(): 
            i = i + 1
            # if i == 1:
            #     continue
            if i == 4:
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
            print("MainPage: ", i)

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
        print("Caregory parsing...")
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
        # print("Viewport Set to 75!")

        # print("--------------------------")
        # print("--------------------------")
        # print("--------------------------")
        # for tag in response.css('select#tag > option ::attr(value)').extract(): 
        #     yield scrapy.FormRequest.from_response( response, formdata={'tag': tag}, callback=self.parse_results, )
    
    def parse_multiple_pages(self, response):
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("Multiple Page Dealers")
        # print(response.body.decode('utf-8'))
        # See how many pages to open in viewport 75

        hrefs = response.xpath('//*[@id="ctl00_MainContent_gwSearch"]//tr[last()]//li/a/@href').extract()
        # pages = response.xpath('/html/body/form/section/div/div/div[1]/div[3]/div/div[2]/table/tbody/tr[76]/td/div/div/ul/li[2]/a').extract()

        print("////////////////////////////////////////////")
        print("parse_multiple_pages---length of pages: ", len(hrefs))
        print("////////////////////////////////////////////")

        j = 0
        # if len(hrefs) == 0:

        #     hrefs.append()

        if len(hrefs) != 0:   
            for href in hrefs:
                j = j + 1
                # href = page.xpath('/@href').extract()
                print("viewport button: ", href)
                print("id of button: ", j)

                eventTarget = href.replace("javascript:__doPostBack('", "").replace("','')", "")
                eventArgument = response.css('#__EVENTARGUMENT::attr(value)').extract()
                lastFocus = response.css('#__LASTFOCUS::attr(value)').extract()
                viewState = response.css('#__VIEWSTATE::attr(value)').extract()
                viewStateGenerator = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract()
                viewStateEncrypted = response.css('#__VIEWSTATEENCRYPTED::attr(value)').extract()
                pageSize = '75'
                sort = '0'

                print(eventTarget)

                # yield scrapy.FormRequest( 

                #     'https://burzarada.hzz.hr/Posloprimac_RadnaMjesta.aspx', 

                #     formdata = { 
                #         '__EVENTTARGET': eventTarget, 
                #         '__EVENTARGUMENT': eventArgument, 
                #         '__LASTFOCUS': lastFocus, 
                #         '__VIEWSTATE': viewState, 
                #         '__VIEWSTATEGENERATOR': viewStateGenerator,
                #         '__VIEWSTATEENCRYPTED': viewStateEncrypted,
                #         'ctl00$MainContent$ddlPageSize': pageSize,
                #         'ctl00$MainContent$ddlSort': sort,
                #     },

                #     callback=self.parse_links 
                    
                # )
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
            yield self.parse_job_list_single(response)
            # self.parse_links(response)

    def parse_links(self, response):
        links = response.xpath('//a[@class="TitleLink"]/@href').extract()
        print("////////////////////////////////////////////")
        print("length of links: ", len(links))
        print("////////////////////////////////////////////")

        k = 0

        for link in links:
            k = k + 1
            link = 'https://burzarada.hzz.hr/' + link
            print("final link: ", link)
            print("job id in one page: ", k)
            yield scrapy.Request(url=link, callback=self.parse_job)

    def parse_job(self, response):

        item = JobsItem()

        print(response)

        """
        url = response.request.url
        title = response.xpath('//*[@id="ctl00_MainContent_pnlAjaxBlock"]//h3//text()').extract_first()
        workplace = response.xpath('//*[@id="ctl00_MainContent_lblMjestoRada"]//text()').extract_first()
        required_workers = response.xpath('//*[@id="ctl00_MainContent_lblBrojRadnika"]//text()').extract_first()
        type_of_employment = response.xpath('//*[@id="ctl00_MainContent_lblVrstaZaposlenja"]//text()').extract_first()
        working_hours = response.xpath('//*[@id="ctl00_MainContent_lblRadnoVrijeme"]//text()').extract_first()
        mode_of_operation = response.xpath('//*[@id="ctl00_MainContent_lblNacinRada"]//text()').extract_first()
        accomodation = response.xpath('//*[@id="ctl00_MainContent_lblSmjestaj"]//text()').extract_first()
        transportation_fee = response.xpath('//*[@id="ctl00_MainContent_lblNaknada"]//text()').extract_first()
        start_date = response.xpath('//*[@id="ctl00_MainContent_lblVrijediOd"]//text()').extract_first()
        end_date = response.xpath('//*[@id="ctl00_MainContent_lblVrijediDo"]//text()').extract_first()
        education_level = response.xpath('//*[@id="ctl00_MainContent_lblRazinaObrazovanja"]//text()').extract_first()
        work_experience = response.xpath('//*[@id="ctl00_MainContent_lblRadnoIskustvo"]//text()').extract_first()
        other_information = response.xpath('//*[preceding-sibling::[@id="ctl00_MainContent_lblOstaleInformacijeText"] and following-sibling::hr]//text()').extract_first()
        employer = response.xpath('//*[@id="ctl00_MainContent_lblNazivPoslodavca"]//text()').extract_first()
        contact = response.xpath('//font[preceding-sibling::[@id="ctl00_MainContent_lblKontaktKandidataText"] and following-sibling::hr]//text()').extract_first()
        driving_test  = response.xpath('//*[@id="ctl00_MainContent_lblVozackiIspit"]//text()').extract_first()       
        """
        """
        item['url'] = url
        item['title'] = title
        item['workplace'] = workplace
        item['required_workers'] = required_workers
        item['type_of_employment'] = type_of_employment
        item['working_hours'] = working_hours
        item['mode_of_operation'] = mode_of_operation
        item['accomodation'] = accomodation
        item['transportation_fee'] = transportation_fee
        item['start_date'] = start_date
        item['end_date'] = end_date
        item['education_level'] = education_level
        item['work_experience'] = work_experience
        item['other_information'] = other_information
        item['employer'] = employer
        item['contact'] = contact
        item['driving_test'] = driving_test

        print(item)

        """
        item['url'] = ''
        item['title'] = ''
        item['workplace'] = ''
        item['required_workers'] = ''
        item['type_of_employment'] = ''
        item['working_hours'] = ''
        item['mode_of_operation'] = ''
        item['accomodation'] = ''
        item['transportation_fee'] = ''
        item['start_date'] = ''
        item['end_date'] = ''
        item['education_level'] = ''
        item['work_experience'] = ''
        item['other_information'] = ''
        item['employer'] = ''
        item['contact'] = ''
        item['driving_test'] = ''

        yield item
    

    def parse_job_list_single(self, response):

        print("no buttons found")
        links = response.xpath('//a[@class="TitleLink"]/@href').extract()
        print("////////////////////////////////////////////")
        print("length of links in id: ", len(links), " in ", j)
        print("////////////////////////////////////////////")

        for link in links:
            link = 'https://burzarada.hzz.hr/' + link
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_job_single)
    

    def parse_job_single(self, response):

        item = JobsItem()

        print(response)

        """
        url = response.request.url
        title = response.xpath('//*[@id="ctl00_MainContent_pnlAjaxBlock"]//h3//text()').extract_first()
        workplace = response.xpath('//*[@id="ctl00_MainContent_lblMjestoRada"]//text()').extract_first()
        required_workers = response.xpath('//*[@id="ctl00_MainContent_lblBrojRadnika"]//text()').extract_first()
        type_of_employment = response.xpath('//*[@id="ctl00_MainContent_lblVrstaZaposlenja"]//text()').extract_first()
        working_hours = response.xpath('//*[@id="ctl00_MainContent_lblRadnoVrijeme"]//text()').extract_first()
        mode_of_operation = response.xpath('//*[@id="ctl00_MainContent_lblNacinRada"]//text()').extract_first()
        accomodation = response.xpath('//*[@id="ctl00_MainContent_lblSmjestaj"]//text()').extract_first()
        transportation_fee = response.xpath('//*[@id="ctl00_MainContent_lblNaknada"]//text()').extract_first()
        start_date = response.xpath('//*[@id="ctl00_MainContent_lblVrijediOd"]//text()').extract_first()
        end_date = response.xpath('//*[@id="ctl00_MainContent_lblVrijediDo"]//text()').extract_first()
        education_level = response.xpath('//*[@id="ctl00_MainContent_lblRazinaObrazovanja"]//text()').extract_first()
        work_experience = response.xpath('//*[@id="ctl00_MainContent_lblRadnoIskustvo"]//text()').extract_first()
        other_information = response.xpath('//*[preceding-sibling::[@id="ctl00_MainContent_lblOstaleInformacijeText"] and following-sibling::hr]//text()').extract_first()
        employer = response.xpath('//*[@id="ctl00_MainContent_lblNazivPoslodavca"]//text()').extract_first()
        contact = response.xpath('//font[preceding-sibling::[@id="ctl00_MainContent_lblKontaktKandidataText"] and following-sibling::hr]//text()').extract_first()
        driving_test  = response.xpath('//*[@id="ctl00_MainContent_lblVozackiIspit"]//text()').extract_first()       
        """
        """
        item['url'] = url
        item['title'] = title
        item['workplace'] = workplace
        item['required_workers'] = required_workers
        item['type_of_employment'] = type_of_employment
        item['working_hours'] = working_hours
        item['mode_of_operation'] = mode_of_operation
        item['accomodation'] = accomodation
        item['transportation_fee'] = transportation_fee
        item['start_date'] = start_date
        item['end_date'] = end_date
        item['education_level'] = education_level
        item['work_experience'] = work_experience
        item['other_information'] = other_information
        item['employer'] = employer
        item['contact'] = contact
        item['driving_test'] = driving_test

        print(item)

        """
        item['url'] = ''
        item['title'] = ''
        item['workplace'] = ''
        item['required_workers'] = ''
        item['type_of_employment'] = ''
        item['working_hours'] = ''
        item['mode_of_operation'] = ''
        item['accomodation'] = ''
        item['transportation_fee'] = ''
        item['start_date'] = ''
        item['end_date'] = ''
        item['education_level'] = ''
        item['work_experience'] = ''
        item['other_information'] = ''
        item['employer'] = ''
        item['contact'] = ''
        item['driving_test'] = ''

        yield item

        # f = open("test.out", 'w')
        # sys.stdout = f
        # print("test")
        # f.close()
    
    # def parse_results(self, response): 
    #     for quote in response.css("div.quote"): 
    #         yield { 'quote': quote.css('span.content ::text').extract_first(), 'author': quote.css('span.author ::text').extract_first(), 'tag': quote.css('span.tag ::text').extract_first(), }
