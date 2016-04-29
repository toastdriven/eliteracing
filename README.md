# Elite Racing Federation

This is the Django project that powers http://edracers.com/, a racing site
focused around the [Elite Dangerous](http://elitedangerous.com/) video game &
the [Elite Racers](http://reddit.com/r/EliteRacers).

It is currently a pre-launch work-in-progress.

**License:** New BSD


## Setup

    # Clone the source
    $ git clone ...
    $ cd eliteracing

    # Setup a virtualenv (to isolate the Python packages installed)
    $ virtualenv env
    $ . env/bin/activate
    $ pip install -r dev_requirements.txt

    # Make sure some (bash) ENV variables are present for the settings
    $ cp simulate_heroku_env.sh.example simulate_heroku_env.sh
    $ source simulate_heroku_env.sh

    # Setup the database
    # As the postgres user
    $ createdb eliteracing

    # As your user
    $ ./manage.py migrate


## Running Locally

    ./manage.py runserver


## Running Tests

`eliteracing` has > `96%` test coverage. Please don't make it worse. :D

    coverage run --omit='env/*' manage.py test --settings=racing.test_settings
    coverage report


## Contributing

Patches are gladly accepted, but must meet the following criteria:

* The contributed work must be your own (no copy-pasta from SO)
* You must agree your work will be license under the project's license (New BSD)
* Any non-HTML/CSS/JS change must have accompanying tests
* You've run the tests & they are all passing

Follow a standard GitHub workflow:

* Hit the "Fork" button on https://github.com/toastdriven/eliteracing
* Clone **your** new repository
* Follow the setup instructions
* **CREATE A NEW BRANCH OFF `master`**
* Make your changes
* Add tests to cover the changes
* Push the branch to your GH repo
* Go back to your repo in browser & use the "Create Pull Request" button

And thanks!
