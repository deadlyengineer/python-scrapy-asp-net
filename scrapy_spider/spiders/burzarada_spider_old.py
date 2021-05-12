# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from ..items import JobsItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JobSpider(scrapy.Spider):

    def __init__(self):
        self.url = 'https://burzarada.hzz.hr/Posloprimac_RadnaMjesta.aspx'
        # self.url = ''

    name = 'burzarada_old'
    # allowed_domains = ['burzarada.hzz.hr']

    def start_requests(self):

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):

        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        options.add_argument("start-maximized")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

        driver.get(self.url)

        print("-----------------------------------------------------------")
        print("-----------------------------------------------------------")
        print("Waiting...")
        
        # driver.implicitly_wait(20)
        delay = 300 # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'footer')))
            print ("Page is ready!")
        except TimeoutException:
            print ("Loading took too much time!")

        print("Waiting finished")
        print("-----------------------------------------------------------")
        print("-----------------------------------------------------------")


        all_links = driver.find_elements_by_css_selector('div.NKZbox > div.KategorijeBox')
        
        print("All anchors: ", len(all_links))

        i = 0

        for x in range(0, len(all_links)):

            print("i: ", i)
            i = i + 1
            print("i: ", i)

            link = driver.find_element_by_css_selector('span.KategorijeBoxHover:nth-of-type(' + str(i) + ')')
            button = link.find_element_by_css_selector('div.NKZbox > div.KategorijeBox')
            button_name = button.find_element_by_tag_name('a').get_attribute('innerHTML')

            if button.is_displayed():

                button.click()

            print("-----------------------------------------------------------")
            print("-----------------------------------------------------------")
            print("Clicked Button: ", button_name)

            print("Waiting...")
            driver.implicitly_wait(20)

            # try:
            #     myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'footer')))
            #     print ("Page is ready!")
            # except TimeoutException:
            #     print ("Loading took too much time!")

            print("***** Link Clicked *****")

            print("Waiting finished")

            print("-----------------------------------------------------------")
            print("-----------------------------------------------------------")

            driver.get(self.url)
            

        #job_page_links = response.css('.job-data a::attr(href)')
        # job_page_links = response.css('.job-title a::attr(href)')
        # yield from response.follow_all(job_page_links, self.parse_job)

    def parse_job(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item = JobsItem()

        url = response.request.url,
        title = response.xpath('normalize-space(//section[@id="page-title"]/h1/text())').get(),
        if "/Details/" in response.request.url:
            source = "Mojposao",
        else:
            source = "Poslovac"
        employer = response.xpath('normalize-space(//li[@class = "job-company"]/text())').get(),
        workplace = response.xpath('normalize-space(//p[@class = "job-location"]/text())').get(),
        start_date = response.xpath('normalize-space(//p[text()[contains(.,"Published")]]/following-sibling::time/text())').get(),
        end_date = response.xpath('normalize-space(//p[@class="deadline"]/time/text())').get(),

        description1 = ' '.join(response.xpath('//div[@id="job-description"]/text()').getall()),
        description2 = ' '.join(response.xpath('//div[@id="job-html"]//*/*[not(self::style or self::script)]/text()').getall()),

        requirements = ' '.join(response.xpath('//div[@id="job-expect"]//*/text()').getall()),
        benefits = ' '.join(response.xpath('//div[@id="job-benefits"]//*/text()').getall()),
        category = ' '.join(response.xpath('//p[text()[contains(.,"Categories:")]]/following-sibling::p/a/text()').getall()),

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

        yield item