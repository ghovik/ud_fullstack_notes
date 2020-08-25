## Create sample data

```python
from app import db, Show, Venue, Artist
from datetime import datetime

a1 = Artist(
  name="GUNS N PETALS",
  city="San Francisco",
  state="CA",
  phone="326-123-5000",
  genres="ROCK N ROLL"
)

a2 = Artist(
  name="MATT QUEVEDO",
  city="New York",
  state="NY",
  phone="300-400-5000",
  genres="JAZZ"
)

a3 = Artist(
  name="THE WILD SAX BAND",
  city="New York",
  state="NY",
  phone="432-325-5432",
  genres="JAZZ"
)

v1 = Venue(
  name="THE MUSICAL HOP",
  address="1015 Folsom Street",
  phone="123-123-1234",
  city="San Francisco",
  state="CA"
)
v2 = Venue(
  name="THE DUELING PIANOS BAR",
  address="335 Delancey Street",
  phone="914-003-1132",
  city="New York",
  state="NY"
)
v3 = Venue(
  name="PARK SQUARE LIVE MUSIC & COFFEE",
  address="34 Whiskey Moore Ave",
  phone="415-000-1234",
  city="San Francisco",
  state="CA"
)

s1 = Show(date=datetime(2020,4,22))
s2 = Show(date=datetime(2021,2,12))
s3 = Show(date=datetime(2022,1,11))

a1.shows = [s1]
a2.shows = [s2]
a3.shows = [s3]
v1.shows = [s1]
v2.shows = [s2]
v3.shows = [s3]

db.session.add(s1)
db.session.add(s2)
db.session.add(s3)
db.session.commit()
```

