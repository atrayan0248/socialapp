from bson import ObjectId
from django.conf import settings


class UserDetails:
    collection_name = 'user_details'

    def __init__(self, age: int, sex: str, interests: list, city: str, user_id: str, _id=None):
        self.age = age
        self.sex = sex
        self.interests = interests
        self.city = city
        self.user_id = user_id
        self._id = _id if _id else ObjectId()

    @classmethod
    def get_collection(cls):
        return settings.DB[cls.collection_name]

    def save(self):
        """
        Inserts or updates a document in the user_details collection
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
        Updates a document in the user_details collection
        """
        collection = self.get_collection()
        document = self.to_dict()

        # Update a document by _id
        if '_id' in document:
            collection.update_many(
                {'_id': self._id},
                {
                    '$set': {
                        'age': self.age,
                        'sex': self.sex,
                        'interests': self.interests,
                        'city': self.city,
                        'user_id': self.user_id,
                    },
                },
            )

    def to_dict(self) -> dict:
        """
        Converts the model instance into a dictionary for MongoDB
        """
        return_data = {
            '_id': self._id,
            'user_id': self.user_id,
            'age': self.age,
            'sex': self.sex,
            'interests': self.interests,
            'city': self.city,
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
        Converts a MongoDB document into an User Details instance
        """
        return cls(
            age=document['age'],
            sex=document['sex'],
            interests=document['interests'],
            city=document['city'],
            user_id=document['user_id'],
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
