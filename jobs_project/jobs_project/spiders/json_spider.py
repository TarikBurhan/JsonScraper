import json
import scrapy
from ..items import JobsItem, TestItem
from datetime import datetime

class Jobpider(scrapy.Spider):
    name = 'json_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'jobs_project.pipelines.JobsProjectPostgrePipeline': 300,
            'jobs_project.pipelines.JobsProjectMongoPipeline': 300,
        },
    }
    

    def __init__(self, **kwargs):
        pass

    def start_requests(self):
        yield scrapy.Request(
            #url='file:////home/s01.json',
            url=r'file:////C:/Users/takos/Desktop/JsonScraper/s01.json',
            callback=self.parse_page,
        )
        yield scrapy.Request(
            #url='file:////home/s02.json',
            url=r'file:////C:/Users/takos/Desktop/JsonScraper/s02.json',
            callback=self.parse_page,
        )
    
    def parse_page(self, response):
        response_json = json.loads(response.text)

        for job in response_json["jobs"]:
            job_item = JobsItem()
            job_data = job["data"]

            job_item["slug"] = job_data.get("slug")
            job_item["language"] = job_data.get("language")
            job_item["languages"] = job_data.get("languages")
            job_item["req_id"] = job_data.get("req_id")
            job_item["title"] = job_data.get("title")
            job_item["description"] = job_data.get("description")
            job_item["street_address"] = job_data.get("street_address")
            job_item["city"] = job_data.get("city")
            job_item["state"] = job_data.get("state")
            job_item["country_code"] = job_data.get("country_code")
            job_item["postal_code"] = job_data.get("postal_code")
            job_item["location_type"] = job_data.get("location_type")
            job_item["latitude"] = job_data.get("latitude")
            job_item["longitude"] = job_data.get("longitude")
            job_item["categories"] = list(map(lambda i: json.dumps(i), job_data.get("categories"))) if job_data.get("categories") != None else None
            job_item["brand"] = job_data.get("brand")
            job_item["department"] = job_data.get("department")
            job_item["recruiter_id"] = job_data.get("recruiter_id")
            job_item["promotion_value"] = job_data.get("promotion_value")
            job_item["salary_value"] = job_data.get("salary_value")
            job_item["salary_min"] = job_data.get("salary_min_value")
            job_item["salary_max"] = job_data.get("salary_max_value")
            job_item["employment_type"] = job_data.get("employment_type")
            job_item["source"] = job_data.get("source")
            job_item["posted_date"] = job_data.get("posted_date")
            job_item["posting_expiry_date"] = datetime.strptime(job_data.get("posting_expiry_date"), "%Y-%m-%dT%H:%M:%S%z") if job_data.get("posting_expiry_date") != None else None
            job_item["apply_url"] = job_data.get("apply_url")
            job_item["is_internal"] = job_data.get("internal")
            job_item["is_searchable"] = job_data.get("searchable")
            job_item["is_applyable"] = job_data.get("applyable")
            job_item["is_li_easy_applyable"] = job_data.get("li_easy_applyable")
            job_item["ats_code"] = job_data.get("ats_code")
            job_item["meta_data"] = json.dumps(job_data.get("meta_data"))
            job_item["update_date"] = datetime.strptime(job_data.get("update_date"), "%Y-%m-%dT%H:%M:%S%z") if job_data.get("update_date") != None else None
            job_item["create_date"] = datetime.strptime(job_data.get("create_date"), "%Y-%m-%dT%H:%M:%S%z") if job_data.get("create_date") != None else None
            job_item["category"] = job_data.get("category")
            job_item["full_location"] = job_data.get("full_location")
            job_item["short_location"] = job_data.get("short_location")
            yield job_item

