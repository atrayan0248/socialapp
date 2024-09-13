from bson import ObjectId
from django.conf import settings


class User:
    collection_name = 'user'

    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
        phone: str,
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
