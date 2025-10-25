import re
import scrapy

from ..items import JobProspects1900Item, JobProspects1900Loader


class Job1900Spider(scrapy.Spider):
    name = "job_1900"
    allowed_domains = ["1900.com.vn"]
    start_urls = ["https://1900.com.vn/viec-lam"]

    def parse(self, response):
        total_pages = int(
            response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[2]/div/nav/ul/li[8]/a/text()").get()
        )
        self.logger.info(f"Total pages found: {total_pages}")

        for page in range(1, total_pages + 1):
            yield scrapy.Request(url=f"https://1900.com.vn/viec-lam?page={page}", callback=self.parse_job_listings)

    def parse_job_listings(self, response):
        job_links = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/a/@href"
        ).getall()
        self.logger.info(f"Found {len(job_links)} job links on the {response.url}.")
        
        for link in job_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_job_details)

    def parse_job_details(self, response):
        timestamp = date.today().isoformat()
        url = response.url
        title = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/span/text()"
        ).get()
        company = (
            response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/a/span")
            .xpath("string()")
            .get()
        )
        number_of_reviews = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div/a/text()"
        ).get()
        number_of_jobs = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div/span[1]/text()"
        ).get()
        views = (
            response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div/span[2]")
            .xpath("string()")
            .get()
        )
        salary = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[1]/strong/text()"
        ).get()
        posted_at = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[3]/strong/text()"
        ).get()
        employement_type = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[5]/strong/text()"
        ).get()
        quantity = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[7]/strong/text()"
        ).get()
        job_title = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/strong/text()"
        ).get()
        application_deadline = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[4]/strong/text()"
        ).get()
        experience = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[6]/strong/text()"
        ).get()
        gender = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[6]/strong/text()"
        ).get()
        job_field = response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[4]/a/text()").get()
        job_department = response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[6]/a/text()").get()
        work_address = " ".join([text.strip() for text in response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[8]/div//text()").getall() if text.strip()])
        job_description = [text.strip() for text in response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[1]//text()").getall() if text.strip()]
        area = " ".join([text.strip() for text in response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[3]/div//text()").getall() if text.strip()])
        company_ref = response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[3]/div[1]/div[2]/div/a/@href").get()
        company_size = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[3]/div[2]/div[1]/div[2]/text()"
        ).get()        
        company_address = response.xpath(
            "/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]/text()"
        ).get()
        company_rating = response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[4]/div[1]/text()").get()
        number_of_reviews = response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[4]/div[2]/text()").get()
        reviews = []
        review_texts = [text.strip() for text in response.xpath("/html/body/div[2]/main/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[2]/div[5]/div/div//text()").getall() if text.strip() and text.strip() != "★"]

        current_review = []
        for text in review_texts:
            if re.match(r'^\d{2}/\d{2}/\d{4}$', text) and current_review:
                reviews.append(' '.join(current_review))
                current_review = [text]
            else:
                current_review.append(text)

        if current_review:
            reviews.append(' '.join(current_review))

        loader = JobProspects1900Loader(item=JobProspects1900Item(), response=response)
        loader.add_value('url', url)
        loader.add_value('title', title)
        loader.add_value('company', company)
        loader.add_value('number_of_reviews', number_of_reviews)
        loader.add_value('number_of_jobs', number_of_jobs)
        loader.add_value('views', views)
        loader.add_value('salary', salary)
        loader.add_value('posted_at', posted_at)
        loader.add_value('employement_type', employement_type)
        loader.add_value('quantity', quantity)
        loader.add_value('job_title', job_title)
        loader.add_value('application_deadline', application_deadline)
        loader.add_value('experience', experience)
        loader.add_value('gender', gender)
        loader.add_value('job_field', job_field)
        loader.add_value('job_department', job_department)
        loader.add_value('work_address', work_address)
        loader.add_value('job_description', job_description)
        loader.add_value('area', area)
        loader.add_value('company_ref', company_ref)
        loader.add_value('company_size', company_size)
        loader.add_value('company_address', company_address)
        loader.add_value('company_rating', company_rating)
        loader.add_value('reviews', reviews)

        yield loader.load_item()
