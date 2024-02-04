# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2
import pymongo
import redis

import sys
from jobs_project import settings
sys.path.append("..")
import query


class JobsProjectPipeline:

    def __init__(self):
        #region Settings

        postgre_hostname = settings.HOSTNAME
        postgre_port = settings.POSTGRESQL_PORT
        postgre_username = settings.POSTGRESQL_USERNAME
        password = settings.POSTGRESQL_PASSWORD
        postgre_database = settings.POSTGRESQL_DATABASE

        mongo_uri = settings.HOSTNAME
        mongo_port = settings.MONGODB_PORT
        mongo_db = settings.MONGODB_DATABASE
        mongo_collection = settings.MONGODB_COLLECTION
        mongo_username = settings.MONGODB_USERNAME
        mongo_password = settings.MONGODB_PASSWORD

        redis_hostname = settings.HOSTNAME
        redis_port = settings.REDIS_PORT

        #endregion

        #region Database Connections

        self.p_connection = psycopg2.connect(host=postgre_hostname, user=postgre_username, password=password, dbname=postgre_database, port=postgre_port)
        self.p_cur = self.p_connection.cursor()
        self.p_cur.execute(query.tableCreateSql)
        self.p_connection.commit()

        self.m_connection = pymongo.MongoClient(mongo_uri, mongo_port, username=mongo_username, password=mongo_password)
        self.m_db = self.m_connection[mongo_db]
        self.m_col = self.m_db[mongo_collection]

        self.redis_conn = redis.Redis(host=redis_hostname, port=redis_port, decode_responses=True)

        #endregion


    def process_item(self, item, spider):
        """
            Writing items to PostgreSql database after checking 
            if given Job Slug Id is not exists in Redis Cache.
        """
        if self.redis_conn.get(item["slug"]) == None:
            self.redis_conn.set(item["slug"], "Exists")
            self.m_col.insert_one(dict(item))
            try:
                self.p_cur.execute(query.insertSql, (item["slug"], item["language"], item["languages"], item["req_id"], item["title"],
                                                item["description"], item["street_address"], item["city"], item["state"],
                                                item["country_code"], item["postal_code"], item["location_type"], item["latitude"],
                                                item["longitude"], item["categories"], item["brand"], item["department"],
                                                item["recruiter_id"], item["promotion_value"], item["salary_value"], item["salary_min"], 
                                                item["salary_max"], item["employment_type"], item["source"], item["posted_date"], 
                                                item["posting_expiry_date"], item["apply_url"], item["is_internal"], item["is_searchable"], 
                                                item["is_applyable"], item["is_li_easy_applyable"], item["ats_code"], item["meta_data"], 
                                                item["update_date"], item["create_date"], item["category"], item["full_location"], 
                                                item["short_location"], ))
                self.p_connection.commit()
            except:
                # Using rollback to if transaction is hung up
                self.p_cur.execute("rollback")
                self.p_cur.execute(query.insertSql, (item["slug"], item["language"], item["languages"], item["req_id"], item["title"],
                                                item["description"], item["street_address"], item["city"], item["state"],
                                                item["country_code"], item["postal_code"], item["location_type"], item["latitude"],
                                                item["longitude"], item["categories"], item["brand"], item["department"],
                                                item["recruiter_id"], item["promotion_value"], item["salary_value"], item["salary_min"], 
                                                item["salary_max"], item["employment_type"], item["source"], item["posted_date"], 
                                                item["posting_expiry_date"], item["apply_url"], item["is_internal"], item["is_searchable"], 
                                                item["is_applyable"], item["is_li_easy_applyable"], item["ats_code"], item["meta_data"], 
                                                item["update_date"], item["create_date"], item["category"], item["full_location"], 
                                                item["short_location"], ))
                self.p_connection.commit()

        return item
    

    def close_spider(self, spider):
        self.p_cur.close()
        self.p_connection.close()
        
        self.m_connection.close()

        self.redis_conn.close()