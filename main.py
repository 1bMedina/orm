############################################################################
## Django ORM Standalone Python Template
############################################################################
""" Here we'll import the parts of Django we need. It's recommended to leave
these settings as is, and skip to START OF APPLICATION section below """

# Turn off bytecode generation
import sys
sys.dont_write_bytecode = True

# Import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm.settings')

# setup django environment
import django
django.setup()

# Import your models for use in your script
from db.models import *


from faker import Faker
from faker.providers import BaseProvider
from faker.providers.internet import BaseProvider
import random
#from django.contrib.auth.models import User
from model_bakery.recipe import Recipe

############################################################################
## START OF APPLICATION
############################################################################
""" Replace the code below with your own """

"""
In case you need to start over. 
Note- this will delete any other tables on the public schema.
Alternatively, you could drop django's tables one-by-one

Login to psql and run these commands in order:

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres, public;

... then migrate again, and re-create your superuser
"""

# Seed a few users in the database
User.objects.create(name='Dan')
User.objects.create(name='Robert')

for u in User.objects.all():
    print(f'ID: {u.id} \tUsername: {u.name}')


fake = Faker()
INT = 'Int'
EXT = 'Ext'
LOCATION_CHOICES = [
        (INT, 'Interior'),
        (EXT, 'Exterior'),
]
BEG = 'Beginner'
EXP = 'Expert'
EXPERIENCE_CHOICES = [
        (BEG, 'Beginner'),
        (EXP, 'Expert'),
]
CL = 'Cold'
HT = 'Hot'
MD = 'Mixed'
CLIMATE_CHOICES = [
        (CL, 'Cold'),
        (HT, 'Hot'),
        (MD, 'Mixed'),
    ]

COOKING = 'Cooking'
HEATING = 'Heating'
OTHER = 'Other'
USE_CHOICES = [
        (COOKING, 'Cooking'),
        (HEATING, 'Heating'),
        (OTHER, 'Other'),
    ]

def fake_dimensions(min_val=1.0, max_val=100.0, precision=2):
    return {
        'width': round(random.uniform(min_val,max_val), precision),
        'height': round(random.uniform(min_val,max_val), precision),
        'depth': round(random.uniform(min_val,max_val), precision)
    }

for i in range(40):
    stoves = Stoves(
        stove_url = fake.domain_name(),
         dimensions = fake_dimensions(), 
         experience = random.choice(EXPERIENCE_CHOICES), 
         price = fake.pydecimal(left_digits = 3, right_digits = 6), 
         climate = random.choice(CLIMATE_CHOICES), 
         stove_location = random.choice(LOCATION_CHOICES), 
         use = random.choice(USE_CHOICES)
         )
    stoves.save()


materialsName = ["steel", "aluminum", "plastic", "rubber", "glass", "carbon fiber", "wood", "ceramic", "leather"]

for i in range(40):
    materials = Materials(
        material_id = fake.uuid4(),
        material_name = random.choice(materialsName),
        stove_id = random.choice(Stoves.objects.all())
    )
    materials.save()

ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
RATING_CHOICES = [
    (ONE, '1'),
    (TWO, '2'),
    (THREE, '3'),
    (FOUR, '4'),
    (FIVE, '5'),
]

for i in range(40):
    reviews = Reviews(
        review_id = fake.uuid4(),
        user_id = random.choice(User.objects.all()),
        stove_id = random.choice(Stoves.objects.all()),
        rating = random.choice(RATING_CHOICES),
        comment = fake.paragraph(nb_sentences = 3),
        created_at = fake.date_time()
    )
    reviews.save()


for i in range(40):
    history = History(
        history_id = fake.uuid4(),
        user_id = random.choice(User.objects.all()),
        stove_id = random.choice(Stoves.objects.all()),
        timestamp = fake.date_time()
    )
    history.save()