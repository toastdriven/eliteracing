# TODO Pre-launch

* (DONE) Install dj_database_url
* (DONE) Setup all the Admins
* (DONE) Finish API

  * Ordering (ascending/descending by date)
  * Filtering

    * By vehicle type (needs an index)
    * By course type (needs an index)
    * By system (needs an index)
    * By CMDR (doesn't need an index! \o/)

  * Pagination
  * Perhaps caching?

* (DONE) Add API docs views
* (DONE) Add E:D license disclaimer to home page footer
* Flesh out the course views

  * List
  * Detail
  * Random Course

* News tests
* Pages tests
* Courses tests
* API tests
* Fix the broken/missing data as much as possible
* Collect screenshots
* Get uploading to S3 working (for local & prod)
* Integrate django-thumbnailer (or similar?)
* Finish HTML/CSS design
* More header shots
* Add in all the original zero gravity series courses
* Add About/Links view
* README for setup/testing/contributions
* Push the code to GitHub (w/ LICENSE)


# TODO Maybe Pre-launch

* Create pages for all the things on the Reddit sub wiki?
* Use some JS/Ractive on the courses for filtering?
* Create EDDB system/station importer (for suggestions/validation in the future)
* Add EDDB links on systems/stations


# TODO Launch

* Check the DNS
* Get settings configured for Heroku
* Set the ENV vars in the Heroku admin
* Get Heroku going & working
* Migrate the DB on Heroku
* Create a superuser for myself, Coconut_head_ & FatHaggard
* Get SES working for error notifications
* Create the announcement

* Investigate SSL cert?


# TODO Post-launch

* Announce on Subreddit
* Announce on Discord
* Announce on main reddit
* Ping EDDB.io for a link (& maybe JS integration on system/station pages?)
* Maybe ping Obsidian Ant for coverage?
* Maybe ping FDev for Community Spotlight?
