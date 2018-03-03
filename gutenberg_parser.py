from lxml import etree
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os

namespaces = {'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
              'pgterms': "http://www.gutenberg.org/2009/pgterms/",
              'dcterms': "http://purl.org/dc/terms/",
              'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
              'dcam': "http://purl.org/dc/dcam/",
              'cc': "http://web.resource.org/cc/"}

class GutenbergParser:
    def __init__(self, host='ds249398.mlab.com', port='49398', 
        db_instance='gutenberg', username='gutenberg', password='ugandaapple'):
        self.host = host
        self.port = port
        self.db_instance = db_instance
        self.username = username
        self.password = password

        self.client = MongoClient('mongodb://' + self.username + ':' + self.password + '@' + 
            self.host + ':' + self.port + '/' + self.db_instance)

    def populate_db(self, values, subjects):
        db = self.client[self.db_instance]
        for key, value in values.items():
            print(key)
            print(value)
                # if key == "language":
                #     data = {"iso_369_1": }
                #     db.language.insert()
    

    def traverse_file_tree(self):
        for dirpath, dirs, files in os.walk("./cache/"):  
            for filename in files:
                fname = os.path.join(dirpath,filename)
                with open(fname) as myfile:
                    values, subjects = self.parse_file(myfile)
                    self.populate_db(values, subjects)


    def parse_file(self, file):
        tree = etree.parse(file)

        xpaths = {"language": "/rdf:RDF/pgterms:ebook/dcterms:language/rdf:Description/rdf:value",
                  "author_name": "/rdf:RDF/pgterms:ebook/dcterms:creator/pgterms:agent/pgterms:name",
                  "author_birth": "/rdf:RDF/pgterms:ebook/dcterms:creator/pgterms:agent/pgterms:birthdate",
                  "author_death": "/rdf:RDF/pgterms:ebook/dcterms:creator/pgterms:agent/pgterms:deathdate",
                  "wiki_link": "/rdf:RDF/rdf:Description",
                  "book_title": "/rdf:RDF/pgterms:ebook/dcterms:title"}
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

        