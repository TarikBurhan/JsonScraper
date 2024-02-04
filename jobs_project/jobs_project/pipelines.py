# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2
import pymongo
import sys

sys.path.append("./")
from jobs_project import settings
sys.path.append("..")
import query

class JobsProjectPostgrePipeline:

    def __init__(self):
        postgre_hostname = settings.HOSTNAME
        postgre_port = settings.POSTGRESQL_PORT
        postgre_username = settings.POSTGRESQL_USERNAME
        password = settings.POSTGRESQL_PASSWORD
        postgre_database = settings.POSTGRESQL_DATABASE

        self.connection = psycopg2.connect(host=postgre_hostname, user=postgre_username, password=password, dbname=postgre_database, port=postgre_port)
        self.cur = self.connection.cursor()
        self.cur.execute(query.tableCreateSql)
        self.connection.commit()


    def process_item(self, item, spider):
        try:
            self.cur.execute(query.insertSql, (item["slug"], item["language"], item["languages"], item["req_id"], item["title"],
                                               item["description"], item["street_address"], item["city"], item["state"],
                                               item["country_code"], item["postal_code"], item["location_type"], item["latitude"],
                                               item["longitude"], item["categories"], item["brand"], item["department"],
                                               item["recruiter_id"], item["promotion_value"], item["salary_value"], item["salary_min"], 
                                               item["salary_max"], item["employment_type"], item["source"], item["posted_date"], 
                                               item["posting_expiry_date"], item["apply_url"], item["is_internal"], item["is_searchable"], 
                                               item["is_applyable"], item["is_li_easy_applyable"], item["ats_code"], item["meta_data"], 
                                               item["update_date"], item["create_date"], item["category"], item["full_location"], 
                                               item["short_location"], ))
            self.connection.commit()
        except:
            self.cur.execute("rollback")
            self.cur.execute(query.insertSql, (item["slug"], item["language"], item["languages"], item["req_id"], item["title"],
                                               item["description"], item["street_address"], item["city"], item["state"],
                                               item["country_code"], item["postal_code"], item["location_type"], item["latitude"],
                                               item["longitude"], item["categories"], item["brand"], item["department"],
                                               item["recruiter_id"], item["promotion_value"], item["salary_value"], item["salary_min"], 
                                               item["salary_max"], item["employment_type"], item["source"], item["posted_date"], 
                                               item["posting_expiry_date"], item["apply_url"], item["is_internal"], item["is_searchable"], 
                                               item["is_applyable"], item["is_li_easy_applyable"], item["ats_code"], item["meta_data"], 
                                               item["update_date"], item["create_date"], item["category"], item["full_location"], 
                                               item["short_location"], ))
            self.connection.commit()

        return item
    

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
        


class JobsProjectMongoPipeline:

    def __init__(self) -> None:
        mongo_uri = settings.HOSTNAME
        mongo_port = settings.MONGODB_PORT
        mongo_db = settings.MONGODB_DATABASE
        mongo_collection = settings.MONGODB_COLLECTION
        mongo_username = settings.MONGODB_USERNAME
        mongo_password = settings.MONGODB_PASSWORD

        self.connection = pymongo.MongoClient(mongo_uri, mongo_port, username=mongo_username, password=mongo_password)
        self.db = self.connection[mongo_db]
        self.col = self.db[mongo_collection]


    def process_item(self, item, spider):
        self.col.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.connection.close()