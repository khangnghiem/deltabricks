import scrapy
from scrapy_playwright.page import PageMethod
from playwright.sync_api import Page

from ..items import JobProspectItem, JobProspectLoader


class VietnamworksSpider(scrapy.Spider):
    name = "vietnamworks"
    allowed_domains = ["www.vietnamworks.com"]
    start_urls = [f"https://www.vietnamworks.com/viec-lam?page={i}" for i in range(1, 3)]
    custom_settings = {
        'CONCURRENT_REQUESTS': 1
    }
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                        PageMethod('wait_for_timeout', 1000),
                    ],
                },
            )

    def parse(self, response):
        # with open('/Users/khangnghiem/Downloads/response.html', 'w', encoding='utf-8') as f:
        # f.write(response.text)
        links = response.xpath(
            "/html/body/div[1]/div[2]/div/div[1]/main/div/div/div/div/div[1]/div[1]/div[3]/div/div/div/div/div[2]/div[1]/div/div/div/h2/a/@href"
        ).getall()
        self.logger.info(f"{len(links)=} links found on {response.url}")

        for link in links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_job,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        # PageMethod("wait_for_timeout", 5000),
                        # PageMethod("wait_for_selector", 'button[aria-label="Xem thêm"]'),
                        # PageMethod("click", 'button[aria-label="Xem thêm"]'),
                        PageMethod("wait_for_timeout", 2000),
                    ],
                },
            )

    async def parse_job(self, response):
        with open('/Users/khangnghiem/Downloads/response_2.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        company_name = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[2]/div/div[1]/div[2]/a/text()").get()
        company_address = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/p/text()").get()
        company_map_link = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/a/@href").get()
        company_size = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/span/text()").get()
        company_contact = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[3]/span/text()").get()
        title = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/h1").get()
        area = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/div[3]/div[3]/div/span/text()").get()
        area = [p.strip() for p in area.split(",")] if area else None
        views = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/div[3]/div[2]/div/span/text()").get()
        expiry_date = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/div[3]/div[1]/div/span/text()").get()
        job_description = response.xpath(
            "/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div/div//text()"
        ).getall()
        job_requirements = response.xpath(
            "/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div//text()"
        ).getall()

        job_posted_date = response.xpath(
            "/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div[1]/div[1]/div/div[2]/p/text()"
        ).get()
        job_department = "".join(
            response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div[1]/div[3]/div/div[2]/p//text()").getall()
        )
        job_field = "".join(
            response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div[1]/div[5]/div/div[2]/p//text()").getall()
        )
        job_minimum_experience = response.xpath(
            "/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div[1]/div[7]/div/div[2]/p/text()"
        ).get()

        # job_minimum_education = response.xpath(
        #     "/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/p/text()"
        # ).get()
        # job_age_preference = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div/div[11]/div/div[2]/p").get()
        # print("Job Minimum Education:", job_minimum_education)
        # print("Job Age Preference:", job_age_preference)
        # print(f"Test: {response.css('button[aria-label=\"Xem thêm\"]').getall()}")
        # print(f"Test: {response.css('button[aria-label="Xem thêm"]').getall()}")

        job_level = "".join(
            response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div[1]/div[2]/div/div[2]/p//text()").getall()
        )
        job_skills = "".join(
            response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div[1]/div[4]/div/div[2]/p//text()").getall()
        )
        document_language = "".join(
            response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div[1]/div[6]/div/div[2]/p//text()").getall()
        )
        nationality = "".join(
            response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[6]/div/div[8]/div/div[2]/p//text()").getall()
        )

        work_address = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[7]/div/div/div/p/text()").get()
        tags = response.xpath("/html/body/main/div/main/div[2]/div/div/div/div[1]/div/div[1]/div/div[8]/div/div[2]/div//text()").getall()

        job_prospect_item = JobProspectLoader(item=JobProspectItem())
        job_prospect_item.add_value("company_name", company_name)
        job_prospect_item.add_value("company_address", company_address)
        job_prospect_item.add_value("company_map_link", company_map_link)
        job_prospect_item.add_value("company_size", company_size)
        job_prospect_item.add_value("company_contact", company_contact)
        job_prospect_item.add_value("title", title)
        job_prospect_item.add_value("area", area)
        job_prospect_item.add_value("views", views)
        job_prospect_item.add_value("expiry_date", expiry_date)
        job_prospect_item.add_value("job_description", [desc.strip() for desc in job_description if desc.strip()])
        job_prospect_item.add_value("job_requirements", [req.strip() for req in job_requirements if req.strip()])
        job_prospect_item.add_value("job_posted_date", job_posted_date)
        job_prospect_item.add_value("job_department", job_department)
        job_prospect_item.add_value("job_field", job_field)
        job_prospect_item.add_value("job_minimum_experience", job_minimum_experience)
        job_prospect_item.add_value("job_level", job_level)
        job_prospect_item.add_value("job_skills", job_skills)
        job_prospect_item.add_value("document_language", document_language)
        job_prospect_item.add_value("nationality", nationality)
        job_prospect_item.add_value("work_address", work_address)
        job_prospect_item.add_value("tags", [tag.strip() for tag in tags if tag.strip()])

        yield job_prospect_item.load_item()
