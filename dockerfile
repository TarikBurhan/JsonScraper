FROM python
COPY . .
RUN pip install -r requirements.txt
ADD ./s01.json ./
ADD ./s02.json ./
WORKDIR /jobs_project
CMD ["scrapy", "crawl", "json_spider"]