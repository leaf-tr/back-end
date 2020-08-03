
import json


class Book(object):
    def __init__(self, isbn, isbn13, title, series_title, image_url, started_at, 
    read_at, date_added, date_updated, read_count, item_type, shelves=[], authors=[]):

        self.isbn = book_data.get('isbn')
        self.isbn13 = book_data.get('isbn13')
        self.title = book_data.get('title_without_series')
        self.series_title = book_data.get('title')
        self.image_url = book_data.get('image_url')
        self.started_at = item_data.get('started_at')
        self.read_at = item_data.get('read_at')
        self.date_added = item_data.get('date_added')
        self.date_updated = item_data.get('date_updated')
        self.read_count = item_data.get('read_count')
        self.item_type = item_type
        self.shelves = shelves
        self.authors = authors

        @staticmethod
        def from_dict(source):
            book = Book(source['isbn'], source['isbn13'], source['title'], source['series_title'],
            source['image_url'], source['started_at'], source['read_at'], source['date_added'], 
            source['date_updated'], source['read_count'], source['item_type'], source['shelves'], source['authors'])

            return book

        def to_dict(self):
            dest = {
                'isbn': self.isbn,
                'isbn13': self.isbn13,
                'title': self.title,
                'series_title': self.series_title,
                'image_url': self.image_url,
                'started_at': self.started_at,
                'read_at': self.read_at,
                'date_added': self.date_added,
                'date_updated': self.date_updated,
                'read_count': self.read_count,
                'item_type': self.item_type,
                'shelves': self.shelves,
                'authors': self.authors
            }

            return dest

        def __repr__(self):
            return(
                Book(\
                    isbn={self.isbn}, \
                    isbn13={self.isbn13}, \
                    title={self.title}, \
                    series_title={self.series_title}, \
                    image_url={self.image_url}, \
                    started_at={self.started_at}, \
                    read_at={self.read_at}, \
                    date_added={self.date_added}, \
                    date_updated={self.date_updated}, \
                    read_count={self.read_count}, \
                    item_type={self.item_type}, \
                    shelves={self.shelves}, \
                    authors={self.authors}\
                )'
            )
