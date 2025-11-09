import scrapy
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Identity
from w3lib.html import remove_tags


class JobProspects1900Loader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip, remove_tags)


class JobProspects1900Item(scrapy.Item):
    timestamp = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    number_of_reviews = scrapy.Field()
    number_of_jobs = scrapy.Field()
    views = scrapy.Field()
    salary = scrapy.Field()
    posted_at = scrapy.Field()
    employement_type = scrapy.Field()
    quantity = scrapy.Field()
    job_title = scrapy.Field()
    application_deadline = scrapy.Field()
    experience = scrapy.Field()
    gender = scrapy.Field()
    job_field = scrapy.Field()
    job_department = scrapy.Field()
    work_address = scrapy.Field()
    job_description = scrapy.Field(output_processor=Identity())
    area = scrapy.Field()
    company_ref = scrapy.Field()
    company_size = scrapy.Field()
    company_address = scrapy.Field()
    company_rating = scrapy.Field()
    reviews = scrapy.Field(output_processor=Identity())

class JobProspectLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip, remove_tags)

class JobProspectItem(Item):
    link = Field()
    title = Field()
    company_name = Field()
    company_address = Field()
    company_map_link = Field()
    company_size = Field()
    company_contact = Field()
    area = Field(output_processor=Identity())
    views = Field()
    expiry_date = Field()
    job_description = Field(output_processor=Identity())
    job_requirements = Field(output_processor=Identity())
    job_posted_date = Field()
    job_department = Field()
    job_field = Field()
    job_minimum_experience = Field()
    job_level = Field()
    job_skills = Field()
    document_language = Field()
    nationality = Field()
    work_address = Field()
    tags = Field(output_processor=Identity())


class CompanyOverviewLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip, remove_tags)


class CompanyOverviewItem(Item):
    link = Field()
    website = Field()
    phone_number = Field()
    department = Field()
    business_type = Field()
    headquarter = Field()
    scale = Field()
    revenue = Field()
    established_at = Field()
    description = Field()
    insurance_policies = Field()
    activities = Field()
    background_history = Field()
    mission = Field()
    parent = Field()
    parent_headquarter = Field()


class CompanyReviewLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip, remove_tags)


class CompanyReviewItem(Item):
    link = Field()
    review_rating = Field()
    review_title = Field()
    review_position = Field()
    review_date = Field()
    pros = Field()
    cons = Field()


class CompanyLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip, remove_tags)


class CompanyItem(Item):
    link = Field()
    name = Field()
    location = Field()
    department = Field()
    scale = Field()
