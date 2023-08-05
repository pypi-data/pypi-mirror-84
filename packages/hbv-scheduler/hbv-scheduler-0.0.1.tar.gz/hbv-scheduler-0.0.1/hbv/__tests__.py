
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# Ensure this import is after sys.path.insert
from hbv import Scheduler as Algorithm


doctors = [
    {
        'id': 0,
        'location': (40.441555, -79.959303)
    },
    {
        'id': 1,
        'location': (40.450735, -79.849049)
    }
]

appointments = [
    {
        'id': 0,
        'location': (40.431905, -79.851548),
        'appt_duration': 20
    },
    {
        'id': 1,
        'location': (40.397651, -79.854818),
        'appt_duration': 20
    },
    {
        'id': 2,
        'location': (40.351140, -79.918702),
        'appt_duration': 20
    },
    {
        'id': 3,
        'location': (40.436660, -80.038563),
        'appt_duration': 20
    },
    {
        'id': 4,
        'location': (40.526031, -80.032424),
        'appt_duration': 20
    },
    {
        'id': 5,
        'location': (40.557981, -79.964831),
        'appt_duration': 20
    },
    {
        'id': 6,
        'location': (40.564547, -79.857867),
        'appt_duration': 20
    },
    {
        'id': 7,
        'location': (40.467258, -79.823765),
        'appt_duration': 20
    },
    {
        'id': 8,
        'location': (40.381547, -79.808720),
        'appt_duration': 20
    },
    {
        'id': 9,
        'location': (40.326893, -79.791233),
        'appt_duration': 20
    },
    {
        'id': 10,
        'location': (40.299249, -79.830516),
        'appt_duration': 20
    },
    {
        'id': 11,
        'location': (40.296740, -79.912396),
        'appt_duration': 20
    },
    {
        'id': 12,
        'location': (40.497490, -79.775845),
        'appt_duration': 20
    },
    {
        'id': 13,
        'location': (40.443608, -79.963201),
        'appt_duration': 20
    },
    {
        'id': 14,
        'location': (40.299249, -79.830516),
        'appt_duration': 20
    },
    {
        'id': 15,
        'location': (40.296740, -79.912396),
        'appt_duration': 20
    },
    {
        'id': 16,
        'location': (40.497490, -79.775845),
        'appt_duration': 20
    },
    {
        'id': 17,
        'location': (40.443608, -79.963201),
        'appt_duration': 20
    },
    {
        'id': 18,
        'location': (40.443608, -79.963201),
        'appt_duration': 20
    }
]

buffer = 10

scheduler = Algorithm(doctors, appointments, buffer)
scheduler.run()
