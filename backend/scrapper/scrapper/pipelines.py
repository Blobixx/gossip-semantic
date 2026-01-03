# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from uuid import uuid4
import psycopg2


class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host="localhost", database="linkup", user="linkup_user", password="password"
        )
        self.db_session = self.conn.cursor()

    def close_spider(self, spider):
        self.db_session.close()
        self.conn.close()

    def process_item(self, item, spider):
        print(f"Pipeline received item: {item['url']}")

        self.db_session.execute(
            """
            INSERT INTO articles
            (uuid, url, title, author, site_name, content, published_at, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (title) DO NOTHING
        """,
            (
                str(uuid4()),
                item["url"],
                item["title"],
                item["author"],
                item["site_name"],
                item["content"],
                item["published_at"],
                item["description"],
            ),
        )
        self.conn.commit()
        return item
