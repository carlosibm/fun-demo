import json
import logging
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from iotfunctions import bif
from ai.functions import DemoHTTPPreload
from iotfunctions.metadata import EntityType
from iotfunctions.db import Database
from iotfunctions.enginelog import EngineLogging
from ai import settings
from scripts.manufacturing_entities import Mfg_Line

EngineLogging.configure_console_logging(logging.DEBUG)

'''
# Replace with a credentials dictionary or provide a credentials
# Explore > Usage > Watson IOT Platform Analytics > Copy to clipboard
# Past contents in a json file.
'''

#with open('credentials.json', encoding='utf-8') as F:
db_schema = 'bluadmin' #  set if you are not using the default
with open('credentials_Monitor-Demo.json', encoding='utf-8') as F:
    credentials = json.loads(F.read())
#db_schema = 'dash100462'  # replace if you are not using the default schema
#with open('credentials_dev2.json', encoding='utf-8') as F:
#    credentials = json.loads(F.read())

'''
Developing Test Pipelines
-------------------------
When creating a set of functions you can test how they these functions will
work together by creating a test pipeline.
'''


'''
Create a database object to access Watson IOT Platform Analytics DB.
'''
db = Database(credentials = credentials)


'''
To do anything with IoT Platform Analytics, you will need one or more entity type.
You can create entity types through the IoT Platform or using the python API as shown below.
The database schema is only needed if you are not using the default schema. You can also rename the timestamp.
'''
entity_type_name = 'Clients'
#db.drop_table(entity_name, schema = db_schema)

entity = Mfg_Line(name = entity_type_name,
                db = db,
                db_schema = db_schema,
                description = "Manufacturing Operations Command Center",
                generate_days = 10,
                drop_existing = False)

entity.register(raise_error=False)
# You must unregister_functions if you change the mehod signature or required inputs.
#db.unregister_functions(["DataHTTPPreload"])
#db.register_functions([DemoHTTPPreload])

entity.exec_local_pipeline()

'''
view entity data
'''
print ( "Read Table of new  entity" )
df = db.read_table(table_name=entity_name, schema=db_schema)
print(df.head())

print ( "Done registering  entity" )
