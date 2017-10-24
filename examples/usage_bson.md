```python
from pymarshal.bson import *
import pymongo

class T(MongoDocument):
   def __init__(self, a, b, _id=None):
     self.a = type_assert(a, int)
     self.b = type_assert(b, int)
     self._id = type_assert(_id, bson.ObjectId, allow_none=True)

>>> t = T(1, 2)
>>> marshal_bson(t)
{'a': 1, 'b': 2}
>>> c = pymongo.MongoClient()
>>> col = c.test_db.test_col
>>> i = col.insert_one(marshal_bson(t))
>>> i.inserted_id
ObjectId('59ee05b5e13823092f8ce542')
>>> a = col.find_one()
>>> b = unmarshal_bson(a, T)
>>> b.__dict__
{'a': 1, 'b': 2, '_id': ObjectId('59ee05b5e13823092f8ce542')}
>>> # Helper method to omit '_id', useful for REST APIs
>>> a.json()
{'a': 1, 'b': 2}
```
