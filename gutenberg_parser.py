import os
import re

from lxml import etree
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os
from pycountry import languages as lan

# TODO:
# add a file hash check in to see if we even want to open the file for parsing

# xml namespaces to be applied to every lxml function for proper parsing
namespaces = {'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
              'pgterms': "http://www.gutenberg.org/2009/pgterms/",
              'dcterms': "http://purl.org/dc/terms/",
              'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
              'dcam': "http://purl.org/dc/dcam/",
              'cc': "http://web.resource.org/cc/"}


class GutenbergParser:
    # currently everything is defaulted since this is for a specific project
    def __init__(self, host='ds249398.mlab.com', port='49398', 
        db_instance='gutenberg', username='gutenberg', password='ugandaapple'):
        self.host = host
        self.port = port
        self.db_instance = db_instance
        self.username = username
        self.password = password

        self.client = MongoClient('mongodb://' + self.username + ':' + self.password + '@' + 
            self.host + ':' + self.port + '/' + self.db_instance)
        self.db = self.client[self.db_instance]


    # This function populates the db for every file.
    def populate_db(self, values, subjects, filename):
        author = {}
        book = {}
        subject_ids = []
        print('file', filename)
        author_related = ["name", "date_of_birth", "date_of_death", "wiki_link"]
        for key, value in values.items():
            # print("value", value)
            if key in author_related:
                author[key] = value
            if key == "language":
                if len(value) == 2:
                    data = {"iso_639_1": value, 
                    "iso_639_2": lan.get(alpha_2=value).alpha_3, 
                    "name": lan.get(alpha_2=value).name }
                else:
                    data = {"iso_639_1": value, 
                    "iso_639_2": value, 
                    "name": value }
                try:
                    lang_id = self.db.language.insert_one(data).inserted_id
                except DuplicateKeyError:

                    lang_id = self.db.language.find_one({"iso_639_1": value}).get("_id")
            elif key == "title":
                book[key] = value
        try:
            author_id = self.db.author.insert_one(author).inserted_id
        except DuplicateKeyError:
            author_id = self.db.author.find_one({'name': author.get('name', None)}).get("_id")
        for subject in subjects:
            try:
                subj_id = self.db.subject.insert_one({'description': subject}).inserted_id
                subject_ids.append(subj_id)
            except DuplicateKeyError:
                subject_ids.append(self.db.subject.find_one({'description': subject}).get('_id'))
        try:
            book['author'] = author_id
            book['language'] = lang_id
            book['subjects'] = subject_ids
            book['number'] = int(re.search(r'\d+', filename).group())
            self.db.book.insert_one(book)
        except DuplicateKeyError:
            pass


    # traverses the file tree of the dowloaded compressed file
    def traverse_file_tree(self, tree="./cache/"):
        for dirpath, dirs, files in os.walk(tree):  
            for filename in files:
                fname = os.path.join(dirpath,filename)
                with open(fname) as myfile:
                    values, subjects = self.parse_file(myfile)
                    self.populate_db(values, subjects, filename)


    # parses the rdf file and passes the relevant info to the db populator.
    def parse_file(self, file):
        tree = etree.parse(file)
        xpaths = {"language": "/rdf:RDF/pgterms:ebook/dcterms:language/rdf:Description/rdf:value",
                  "name": "/rdf:RDF/pgterms:ebook/dcterms:creator/pgterms:agent/pgterms:name",
                  "date_of_birth": "/rdf:RDF/pgterms:ebook/dcterms:creator/pgterms:agent/pgterms:birthdate",
                  "date_of_death": "/rdf:RDF/pgterms:ebook/dcterms:creator/pgterms:agent/pgterms:deathdate",
                  "wiki_link": "/rdf:RDF/rdf:Description",
                  "title": "/rdf:RDF/pgterms:ebook/dcterms:title"}
        values = {}
        for key, value in xpaths.items():
            xpath = None
            if key == "wiki_link":
                try:
                    xpath = tree.xpath(value, namespaces=namespaces)[0].attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
                except:
                    pass    
            else:
                try:
                    xpath = tree.xpath(value, namespaces=namespaces)[0].text
                except:
                    pass
            if xpath:
                values[key] = xpath
        subjects_text = []
        subjects = tree.findall('.//dcterms:subject', namespaces=namespaces)
        for subject in subjects:
            subjects_text.append(subject.find('.//rdf:Description/rdf:value', namespaces=namespaces).text)
        return values, subjects_text
