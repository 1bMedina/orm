import sys
import os
import time
import random
from faker import Faker
from django.db import transaction


# Django setup stuff
# Note: Don't re-order these lines or weird stuff will happen
sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
import django

django.setup()
from db.models import *

####
#  Part 1: Generate lots of fake data
#
#   The faker code that we wrote before was pretty inefficient
#   This code is similar, but has some tweaks that make it way faster
#
####
fake = Faker()


# Function to create random latitude and longitude within DC area
def random_latitude():
    return round(random.uniform(38.5, 39.5), 6)


def random_longitude():
    return round(random.uniform(-77.5, -76.5), 6)


places = []
owners = list(User.objects.all())

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
for _ in range(100):  # CHANGE THIS VALUE to test different table sizes
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

with transaction.atomic():
    Stoves.objects.bulk_create(places, batch_size=500)  # Adjust batch_size as needed


####
#  Part 2: Run both versions of the query a bunch of times,
#   and print a summary
####


def test_query_exact():
    start = time.perf_counter()
    s = Stoves.objects.filter(use="'Cooking'").count()
    end = time.perf_counter()
    return end - start


def test_query_iexact():
    start = time.perf_counter()
    s = Stoves.objects.filter(use__iexact="'Cooking'")
    print(s)
    end = time.perf_counter()
    return end - start


exact_times = []
iexact_times = []

for _ in range(50):  # Change this value to change sample size
    exact_times.append(test_query_exact())
    iexact_times.append(test_query_iexact())


num_records = Stoves.objects.all().count()
avg_exact = round(sum(exact_times) / len(exact_times), 3)
avg_iexact = round(sum(iexact_times) / len(iexact_times), 3)


print(f"With {num_records} records in the table:")
print(f"\t- average time for query that uses index: {avg_exact} seconds")
print(f"\t- average time for query that does not use index: {avg_iexact} seconds")