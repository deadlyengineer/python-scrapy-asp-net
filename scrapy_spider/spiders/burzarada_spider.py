import scrapy
from scrapy_spider.items import JobsItem

pageSize = '75'
sort = '0'
category_number = 1
job_category = ''

class JobSpider(scrapy.Spider): 
    
    name = 'burzarada' 
    start_urls = ['https://burzarada.hzz.hr/Posloprimac_RadnaMjesta.aspx'] 
    download_delay = 0.5

    def parse(self, response): 

        iter = 0
        for href in response.css('div.NKZbox > div.KategorijeBox > a ::attr(href)').extract(): 
            
            iter = iter + 1
            if iter != category_number:
                continue

            job_categories = response.css('div.NKZbox > div.KategorijeBox > a ::text').extract()
            global job_category
            job_category= job_categories[category_number - 1]
            # Getting form data
            eventTarget = href.replace("javascript:__doPostBack('", "").replace("','')", "")
            eventArgument = response.css('#__EVENTARGUMENT::attr(value)').extract()
            lastFocus = response.css('#__LASTFOCUS::attr(value)').extract()
            viewState = response.css('#__VIEWSTATE::attr(value)').extract()
            viewStateGenerator = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract()
            viewStateEncrypted = response.css('#__VIEWSTATEENCRYPTED::attr(value)').extract()

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


    def parse_multiple_pages(self, response):

        hrefs = response.xpath('//ul[contains(@class, "pagination")]//a/@href').extract()

        if len(hrefs) != 0:   

            for href in hrefs:

                eventTarget = href.replace("javascript:__doPostBack('", "").replace("','')", "")
                eventArgument = response.css('#__EVENTARGUMENT::attr(value)').extract()
                lastFocus = response.css('#__LASTFOCUS::attr(value)').extract()
                viewState = response.css('#__VIEWSTATE::attr(value)').extract()
                viewStateGenerator = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract()
                viewStateEncrypted = response.css('#__VIEWSTATEENCRYPTED::attr(value)').extract()

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

            requests_for_job_details = self.parse_links(response)

            for request in requests_for_job_details:

                yield request

    def parse_links(self, response):
        
        links = response.xpath('//a[@class="TitleLink"]/@href').extract()

        for link in links:

            link = 'https://burzarada.hzz.hr/' + link
            yield scrapy.Request(url=link, callback=self.parse_job)

    def parse_job(self, response):

        item = JobsItem()

        global job_category
        category = job_category

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
        other_information = ' '.join(response.xpath('//*[@id="ctl00_MainContent_lblOstaleInformacijeText"]/following-sibling::text()').getall())
        employer = response.xpath('//*[@id="ctl00_MainContent_lblNazivPoslodavca"]//text()').extract_first()
        contact = ' '.join(response.xpath('//*[@id="ctl00_MainContent_lblKontaktKandidataText"]/following-sibling::ul//text()').getall())
        driving_test  = response.xpath('//*[@id="ctl00_MainContent_lblVozackiIspit"]//text()').extract_first()       

        item['url'] = url
        item['category'] = category
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

        yield item