# Architecture

* Back-end written in Python using the Django web framework
* Database will be PostgreSQL
* Heavily API-driven (using `restless`)
* Front-end written in mostly JS (using `Ractive`) & hitting the API
* Initially use Bootstrap (or whatever the flavor of the month is)
* All users get an API token
  * for eventually creating data via the site JS
  * may need a separate token to allow public API access?

* Hosted on Heroku for ease
* Static assets on S3 (?)
* Maybe OSS the whole thing?
