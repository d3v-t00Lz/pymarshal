```python
import datetime
from pymarshal.bson import *
import pymongo

class T(MongoDocument):
   def __init__(self, a, b, dt=None, _id=None):
     self.a = type_assert(a, int)
     self.b = type_assert(b, int)
     self.dt = type_assert(
         dt,
         datetime.datetime,
         dynamic=datetime.datetime.now(),
     )
     self._id = type_assert(_id, bson.ObjectId, allow_none=True)

>>> t = T(1, 2)
>>> marshal_bson(t)
{
  'a': 1,
  'b': 2,
  'dt': datetime.datetime(2017, 11, 3, 9, 9, 4, 314685)
}
>>> c = pymongo.MongoClient()
>>> col = c.test_db.test_col
>>> i = col.insert_one(marshal_bson(t))
>>> i.inserted_id
ObjectId('59ee05b5e13823092f8ce542')
>>> a = col.find_one()
>>> b = unmarshal_bson(a, T)
>>> b.__dict__
{
  'a': 1,
  'b': 2,
  'dt': datetime.datetime(2017, 11, 5, 9, 9, 4, 314685),
  '_id': ObjectId('59ee05b5e13823092f8ce542')
}
>>> # Helper method to optionally omit '_id', and cast datetime objects
# to either JSON string or float UNIX timestamp, useful for REST APIs
>>> b.json()
{
  'a': 1,
  'b': 2,
  'dt': 1509901744.314685
}
```
