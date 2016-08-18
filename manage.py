from flask_script import Manager, prompt_bool
from nls import app, models
import requests
from mongoengine import connect, DoesNotExist
from time import sleep
from slugify import slugify
import re
import os
import csv
import random
from datetime import date, timedelta, time, datetime

manager = Manager(app)

@manager.command
def resetdatabase():
    "Delete all data, reset everything"
    if prompt_bool("Are you absolutely certain you want to delete all this things?"):

      db = connect(app.config['MONGODB_DB'], host=app.config['MONGODB_HOST'],  port=app.config['MONGODB_PORT'])
      db.drop_database(app.config['MONGODB_DB'])
      print("Deleted all collections from database ...")

@manager.command
def importevents():
    
    #get all libraries
    libraries = models.Library.objects()

    #add them randomly 10 times
    for i in range(10):
        #get list of example events
        f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/events.csv'))
        for row in csv.reader(f):

            #create a random date in next few week
            event_date = date.today() + timedelta(days=random.randrange(0, 35))
            event_time = time(random.randrange(10, 18), random.choice([00, 30]))

            #save event
            event = models.Event()
            event.title = row[0]
            event.category = row[1]
            event.library = libraries[random.randrange(0, len(libraries) - 1 )]
            event.occurs_at = datetime.combine(event_date, event_time)
            event.save()


@manager.command
def importlibraries():
    response = requests.get("http://www.derbyshire.gov.uk/Common/map_geojson/dataStore/libraries/all_libraries.asp")
    data = response.json()
    for item in data['features']:

        #title
        library = models.Library()
        library.name = "%s Library" % item['properties']['Library'].title()
        library.slug = slugify(library.name)

        #address
        address_formatted = ""
        address_split = item['properties']['Address'].split('</br>')
        count = 0
        for line in address_split:
            count += 1
            if not line.replace('\n', '').strip() == "":
                if count == len(address_split) - 1:
                    address_formatted = "%s %s," % (address_formatted, line.upper())
                elif count != len(address_split):
                    address_formatted = "%s %s," % (address_formatted, line.title())
        library.address = address_formatted.strip().strip(',')
        
        #location
        library.lnglat = [item['geometry']['coordinates'][1], item['geometry']['coordinates'][0]]

        #authority
        library.library_authority = "Derbyshire County Council"
        library.accountable_councillor = "Councillor Kevin Maton"

        #image
        image_dir = "%s/nls/static/images/libraries/" % os.path.dirname(os.path.abspath(__file__))
        image_file_name = item['properties']['Photo'].split("/")[len(item['properties']['Photo'].split("/")) - 1]
        photo_url = "http://www.derbyshire.gov.uk%s" % item['properties']['Photo']
        response = requests.get(photo_url)
        with open("%s%s" % (image_dir, image_file_name), 'wb') as image:
            image.write(response.content)
        library.image_file_name = image_file_name

        #save
        library.save()

@manager.command
def importall():
    resetdatabase()
    importlibraries()
    importevents()


# @manager.command
# def temp():

#     legislations = models.Legislation.objects()
#     for legislation in legislations:
#         for tag in list(legislation._tags):
#             if tag.key == 'user':
#                 legislation._tags.remove(tag)
#         legislation.save()

if __name__ == "__main__":
    manager.run()