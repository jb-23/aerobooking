# Aerobooking - Aircraft Booking System

This project demonstrates an MVP version of an aircraft booking system, such as
are used for managing aircraft flying schedules at flying schools and aeroclubs.

It is written in Python using the web framework Django.

A live version of this project can be seen working at
<http://aerobooking.bamfordresearch.com/>.


## Running on your local machine

- The following assumes you have cloned this repository into a new directory
  and set up a virtual environment with Virtualenv.
- cd into the aerobooking directory
- Install Django and other requirements by running
  `pip install -r deploy_tools/requirements.txt`
- Create the database by running `python manage.py makemigrations`
  and `python manage.py migrate`
- Load user and aircraft data into the database with
  `python manage.py loaddata bookings/0000_mvp_fixture.json`
- Run the test server with `python manage.py runserver`
- Visit the site on your local machine at <http://localhost:8000/>


### Further Information

Please visit my blog at <http://www.bamfordresearch.com/>


### Copyright

Aerobooking copyright (c) 2021 Jason Bamford.

This software is provided "as is" and without any express or implied
warranties, including, without limitation, the implied warranties of
merchantability and fitness for a particular purpose.
