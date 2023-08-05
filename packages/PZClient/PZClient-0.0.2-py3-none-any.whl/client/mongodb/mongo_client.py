from pymongo import MongoClient
from typing import List, Dict


class Mongo:
    CONNECTION_STRING = "mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"

    def __init__(self, host: str, username: str, password: str, database: str = None,
                 collection: str = None):
        self._client = MongoClient(Mongo.CONNECTION_STRING.format(host=host, username=username, password=password))
        self._database = self._client[database] if database else None
        self._collection = self._database[collection] if database and collection else None

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database: str):
        self._database = self._client[database]

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, collection: str):
        if self._database:
            self._collection = self._database[collection]
        else:
            raise Exception("You must set database first.")

    def _get_right_database(self, database: str):
        return self._database if self._database.name == database else self._client[database]

    def _get_right_collection(self, collection: str, database: str):
        if collection is None and database is None:
            return self._collection

        if database and not collection:
            raise Exception("You must give a collection while changing a database.")

        if database is None:
            return self._database[collection]

        db = self._get_right_database(database)
        if self.database is db:
            return self._collection if self._collection.name == collection else self._database[collection]
        else:
            return db[collection]

    def add_document(self, document: Dict, collection: str = None, database: str = None):
        """
        Adds a single document. Optional - user other collection or database than default
        :param document: { "name": "ram", "age": 21 }
        :param collection: test
        :param database: test
        :return: Inserted ObjectIds.
        """
        return self._get_right_collection(collection, database).insert_one(document).inserted_id

    def add_bulk(self, documents: List[Dict], collection: str = None, database: str = None):
        """
        Added multiply documents in a single request. Optional - user other collection or database than default
        :param documents: { "name": "ram", "age": 21 }
        :param collection: test
        :param database: test
        :return: Return a list of ObjectIds.
        """
        return self._get_right_collection(collection, database).insert_many(documents).inserted_ids

    def get_single_document(self, query: str = {}, sort_field=None, asc=True, collection: str = None,
                            database: str = None):
        """
        Returns the first document matches the query. Optional - use other collection or database than default.
        :param query: { "age": 21 }
        :param sort_field: "priority"
        :param asc: True/False
        :param collection: test
        :param database: test
        :return: The first document matching the query.
        """
        result = self._get_right_collection(collection, database).find(query)
        if sort_field:
            direction = 1 if asc else -1
            result.sort(sort_field, direction)
        return result.limit(1)[0] if result.count() else None

    def get_documents(self, query: str = {}, sort_field=None, asc=True, collection: str = None, database: str = None):
        """
        Returns documents by query. Optional - use other collection or database than default.
        :param query: { "age": 21 }
        :param sort_field: "priority"
        :param asc: True/False
        :param collection: test
        :param database: test
        :return: A list object with all matching documents.
        """
        result = self._get_right_collection(collection, database).find(query)
        if sort_field:
            direction = 1 if asc else -1
            result.sort(sort_field, direction)
        return result

    def update_document(self, values: str, query: str = {}, collection: str = None, database: str = None):
        """
        Update documents by query and  values to update. Optional - use other collection or database than default.
        :param values: { "$set": { "name": "Minnie" } }
        :param query: { "age": 21 }
        :param collection: test
        :param database: test
        :return: The number of documents updated.
        """
        return self._get_right_collection(collection, database).update_many(query, values).modified_count

    def remove_single_document(self, query: str, collection: str = None, database: str = None):
        """
        Remove the first document that matches the query. Optional - use other collection or database than default.
        :param query: { "age": 21 }
        :param collection: test
        :param database: test
        :return: The number of documents deleted.
        """
        return self._get_right_collection(collection, database).delete_one(query).deleted_count

    def remove_documents(self, query: str, collection: str = None, database: str = None):
        """
        Removes all the documents that matches the query. Optional - use other collection or database than default.
        :param query: { "age": 21 }
        :param collection: test
        :param database: test
        :return: The number of documents deleted.
        """
        return self._get_right_collection(collection, database).delete_many(query).deleted_count

    def get_document_and_remove(self, query: str = {}, collection: str = None, database: str = None):
        """
        Returns the first document that matched the query and removed it afterwards.
        Optional - use other collection or database than default.
        :param query: { "age": 21 }
        :param collection: test
        :param database: test
        :return: The document that was removed.
        """
        return self._get_right_collection(collection, database).find_one_and_delete(query)

    def get_document_count(self, query: str = {}, collecton: str = None, database: str = None):
        """
        Returns the count of documents matches the query.
        Optional - use other collection or database than default.
        :param query: { "age": 21 }
        :param collecton: test
        :param database: test
        :return: The number of documents matches the query.
        """
        return self._get_right_collection(collecton, database).count_documents(query)

    def get_collection_size(self, collection: str = None, database: str = None):
        """
        Return the size in byte of the collection.
        Optional - use other collection or database than default.
        :param collection: test
        :param database: test
        :return: The size in Bytes of the collection.
        """
        return self._database.command("collstats", self._collection.name)["size"]
