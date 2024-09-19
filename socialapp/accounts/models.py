from datetime import datetime

from bson import ObjectId
from django.conf import settings


class Token:
    collection_name = 'token'

    def __init__(self, token: str, blacklisted_at=datetime.utcnow(), _id=None):
        self.token = token,
        self.blacklisted_at = blacklisted_at
        self._id = _id if _id else ObjectId()

    @classmethod
    def get_collection(cls):
        return settings.DB[cls.collection_name]

    def save(self):
        """
        Inserts a document in a mongodb collection
        """
        collection = self.get_collection()
        document = self.to_dict()

        # Insert a new token to blacklist

        collection.insert_one(document)

    def to_dict(self) -> dict:
        """
        Converts the model instance into a dictionary for MongoDB
        """
        return_data = {
            'token': self.token,
            'blacklisted_at': self.blacklisted_at,
            '_id': self._id,
        }
        return return_data

    @classmethod
    def find(cls, query):
        """
        Find documents in the collection matching the query
        """
        collection = cls.get_collection()
        return [cls.from_dict(doc) for doc in collection.find(query)]

    @classmethod
    def from_dict(cls, document):
        """
        Converts a MongoDB Document into a User instance
        """
        return cls(
            token=document['token'],
            blacklisted_at=document['blacklisted_at'],
            _id=document['_id'],
        )

    @classmethod
    def find_one(cls, query):
        """
        Finds a single document in the collection matching the query
        """
        collection = cls.get_collection()
        document = collection.find_one(query)

        if document:
            return cls.from_dict(document)

        return None

    @classmethod
    def delete(cls, query):
        """
        Deletes documents from the collection matching the query
        """
        collection = cls.get_collection()
        collection.delete_many(query)

    @property
    def id(self):
        return self._id


class User:
    collection_name = 'user'

    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        phone: str,
        password: bytes,
        country_code: str,
        _id=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.country_code = country_code
        self._id = _id if _id else ObjectId()

    @classmethod
    def get_collection(cls):
        return settings.DB[cls.collection_name]

    def save(self):
        """
        Inserts or updates a document in a mongodb collection
        """
        collection = self.get_collection()
        document = self.to_dict()

        # Decide whether to insert or update
        if '_id' in document:
            collection.replace_one({'_id': self._id}, document, upsert=True)
        else:
            collection.insert_one(document)

    def update(self):
        """
        Updates a document in a mongodb collection
        """
        collection = self.get_collection()
        document = self.to_dict()

        # Update a document by _id

        if '_id' in document:
            collection.update_many(
                {'_id': self.id},
                {
                    '$set': {
                        'first_name': self.first_name,
                        'last_name': self.last_name,
                        'username': self.username,
                        'email': self.email,
                        'phone': self.phone,
                        'country_code': self.country_code,
                    },
                },
            )

    def to_dict(self) -> dict:
        """
        Converts the model instance into a dictionary for MongoDB
        """
        return_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'country_code': self.country_code,
            '_id': self._id,
        }
        return return_data

    @classmethod
    def find(cls, query):
        """
        Find documents in the collection matching the query
        """
        collection = cls.get_collection()
        return [cls.from_dict(doc) for doc in collection.find(query)]

    @classmethod
    def from_dict(cls, document):
        """
        Converts a MongoDB Document into a User instance
        """
        return cls(
            first_name=document['first_name'],
            last_name=document['last_name'],
            username=document['username'],
            email=document['email'],
            password=document['password'],
            phone=document['phone'],
            country_code=document['country_code'],
            _id=document['_id'],
        )

    @classmethod
    def find_one(cls, query):
        """
        Finds a single document in the collection matching the query
        """
        collection = cls.get_collection()
        document = collection.find_one(query)

        if document:
            return cls.from_dict(document)

        return None

    @classmethod
    def delete(cls, query):
        """
        Deletes documents from the collection matching the query
        """
        collection = cls.get_collection()
        collection.delete_many(query)

    @property
    def id(self):
        return self._id
