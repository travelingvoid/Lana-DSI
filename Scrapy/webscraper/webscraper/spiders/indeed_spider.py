import scrapy
from webscraper.items import  WebscraperItem


class IndeedSpider(scrapy.Spider):
    name = "indeed_spider"
    allowed_domains = ["indeed.com"]


    # job query key terms 
    job_sites = ["https://www.indeed.com/jobs"]
    job_titles = ["Data Scientist", 'Machine Learning Engineer', "Data Analyst"]
    citites_stats = [("San Francisco", "CA"), ("Los Angeles", "CA"), ("San Diego", "CA")]

    # increment page in order to scrap additonal posting in same city
    page_increment_list = ['0','1','2']

    # list populated with unique combinations of job query key terms
    #these combinations form unique urls to scrap 
    start_urls = self.build_indeed_url(job_sites, job_titles, citites_stats)
    

#     start_urls = (
#         'https://www.indeed.com/jobs?q=Data+Scientist&l=San+Bernardino%2C+CA&start=2',
#     )

    def fill_url_list(self, job_sites, job_titles, citites_stats):
        '''Return a list with every combination of urls for job searchs. 
        Each combination mush as job_site, job_titles, and cities_states in this format:

        https://www.indeed.com/jobs?q=Data+Scientist&l=San+Bernardino%2C+CA'''

        # you will need to call build_url inside this function

        pass


    def build_indeed_url(self, site, job_title, citites_stats, incremental_page = None):
        '''Build site url template with specifc arguments.
           Return a correct url address that can be used to request an Indeed page. 
           The url should be able to work on the chrome browser'''

        pass 


    def parse(self, response):
        titles = response.xpath('//h2/a/@title').extract()
        links = response.xpath('//h2/a/@href').extract()
        companies = response.xpath('//span[@class="company"]/span/text()').extract()

        for title, link, comp in zip(titles, links, companies):
            item = WebscraperItem()
            item['title'] = title
            abs_url = response.urljoin(link)
            item['url'] = abs_url
            item['company'] = comp

            request = scrapy.Request(abs_url, callback=self.parse_job)
            request.meta['item'] = item
            yield request


    def parse_job(self, response):
        item = response.meta['item']
        keys = ['sql', 'python', 'ml', 'spark', 'hadoop', 'dl',
                'stats', 'ts', 'de', 'dp', 
                'nlp', 'bd', 'pca', 'pred_modeling', 
                'anomaly_detection', 'data_analysis', 
                'exp_design', 'cnn', 'bayes_opt', 'pipeline']

        skills = ['sql', 'python', 'machine learning',
                  'spark', 'hadoop', 'deep learning', 
                  'statistics', 'time series', 'data engineering', 
                  'data products', 'nlp', 'big data', 
                  'pca', 'predictive modeling', 'anomaly detection', 
                  'data analysis', 'experimental design', 
                  'deep convolutional networks','bayesian optimization',
                  'pipeline']

        for key, skill in zip(keys, skills):
            item[key] = int(skill in response.text.lower())

        yield item
