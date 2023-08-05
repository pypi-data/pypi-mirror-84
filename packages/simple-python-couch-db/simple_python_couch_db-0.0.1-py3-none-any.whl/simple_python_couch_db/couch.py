import requests, json, re

__all__ = ["Couch", "Database"]

class Couch:
    """Handles the connection to CouchDB and any interaction with databases
    """
    def __init__(self, user, password, host="localhost", port="5984"):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        
    def get_url(self):
        """Creates the url needed to access CouchDB

        Returns:
            str: URL-String to access CouchDB
        """
        return f'http://{self.user}:{self.password}@{self.host}:{self.port}'
            
    def connect(self):
        """Sends CouchDBs welcome message in order to check connectivity

        Returns:
            dict: Dict containing the welcome message from CouchDB
        """
        return requests.get(self.get_url()).json()
    
    def has_database(self, db_name):
        """Checks whether a database is already existent on CouchDB

        Args:
            db_name (str): Name of the database

        Returns:
            boolean: True if the database exists. False if it doesn't exist
        """
        return True if requests.get(f'{self.get_url()}/{db_name}').status_code is 200 else False
    
    def get_database(self, db_name):
        """Retrieves a Database-Object if the database can be found on CouchDB

        Args:
            db_name (str): Name of the database

        Raises:
            ValueError: If the name doesn't exist an error is raised

        Returns:
            Database: Database-Object for further handling
        """
        if not self.has_database(db_name):
            raise ValueError(f'The database "{db_name}" doesn\'t exist.')
        
        return Database(db_name, self)

    def create_database(self, db_name):
        """Creates a new database on CouchDB

        Args:
            db_name (str): Name of the database

        Raises:
            ValueError: If db_name doesn't meet the naming requirements this error is raised

        Returns:
            dict: Answer from CouchDB
        """
        if not re.fullmatch(r"^[a-z][a-z0-9_$()+/-]*$", db_name):
            raise ValueError(f'The database name "{db_name}" does not match the criteria. It must start with a lowercase letter a-z, can contain lowercase letters (a-z), digits (0-9) or any of these _, $, (, ), +, -, and /.')
        r = requests.put(f'{self.get_url()}/{db_name}')
        return r.json()

    def delete_database(self, db_name):
        """Deletes a database from CouchDB

        Args:
            db_name (str): Name of the database

        Returns:
            dict: Answer from CouchDB
        """
        r = requests.delete(f'{self.get_url()}/{db_name}')
        return r.json()
    
class Database:
    """Database from CouchDB. Handles all interactions with documents
    """
    def __init__(self, name, couch):
        self.name = name
        self.couch = couch
    
    def get_db_url(self):
        """Constructs the URL for this particular database

        Returns:
            str: URL-string for the database based on the Couch-Session
        """ 
        return f'{self.couch.get_url()}/{self.name}'
        
    def get_document_url(self, document_id):
        """Constructs an URL leading to a document

        Args:
            document_id (str): ID of the document

        Returns:
            str: URL-string for a document
        """
        return f'{self.get_db_url()}/{document_id}'
        
    def has_document(self, document_id):
        """Checks whether a documents exists

        Args:
            document_id (str): ID of the document

        Returns:
            boolean: True if the document is in the database. False if it is not
        """
        return True if requests.get(self.get_document_url(document_id)).status_code is 200 else False
    
    def get_all_document_ids(self):
        """Retrieves all document ids on a database

        Returns:
            list: List of document IDs
        """
        rows = requests.get(f'{self.get_db_url()}/_all_docs').json()['rows']
        return [r['id'] for r in rows]
    
    def get_document(self, document_id):
        """Retrieves a document from the database

        Args:
            document_id (str): ID of the document

        Raises:
            ValueError: If the document ID is not existent this error is raised

        Returns:
            dict: Document as dictionary
        """
        if not self.has_document(document_id):
            raise ValueError(f'The database {self.name} doens\'t hold a document with the id {document_id}')
        return requests.get(self.get_document_url(document_id)).json()
    
    def save_document(self, document):
        """Saves a document to the database if it has _rev otherwise creates the new document.
        If _id is passed as a field it will use _id as document id. Otherwise a uuid will be created and returned.

        Args:
            document (dict): Document 

        Raises:
            ValueError: If the revision of the document is too old this error is raised.
            RuntimeError: If 400, 404 or 405 status codes are returned this error is raised

        Returns:
            dict: Answer from CouchDB. Contains the id if no id was passed with document
        """
        r = requests.put(self.get_document_url(document['_id']), data=json.dumps(document))
        if r.status_code is 409:
            raise ValueError(f'The document with the id "{document["_id"]}" could not be updated since no changes were made.')
        elif not r.status_code in [200, 201]:
            raise RuntimeError(f'The document with the id "{document["_id"]}" could not be updated')
        return r.json()
                               
    def delete_document(self, document):
        """Deletes a document from the database.

        Args:
            document (dict): Document

        Raises:
            ValueError: If it is an older revision 409 is triggered.
            ValueError: If the ID of the document is incorrect, it will trigger this error as CouchDB answers with 404 - Not Found
            RuntimeError: If any other error happened on CouchDB it will answer with this error

        Returns:
            dict: Answer from CouchDB
        """
        r = requests.delete(f'{self.get_document_url(document["_id"])}?rev={document["_rev"]}')
        if r.status_code is 409:
            raise ValueError(f'The document with the id "{document["_id"]}" could not be deleted since it isn\'t the most recent revision.')
        elif r.status_code is 404:
            raise ValueError(f'The document with the id "{document["_id"]}" does not exists.')
        elif r.status_code not in [200, 201]:
            raise RuntimeError(f'The document with the id "{document["_id"]}" could not be deleted')
        return r.json()
        
    def get_all_documents(self):
        """Retrieves all documents in this database.

        Returns:
            list: List of documents
        """
        document_keys = self.get_all_document_ids()
        data = {'docs': [{'id': d} for d in document_keys]}
        documents = requests.post(f'{self.get_db_url()}/_bulk_get', json=data)
        return documents.json()