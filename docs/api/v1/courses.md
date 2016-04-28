# Courses API

This API uses a HTTP transport, using REST-style verbs for data access.

All requests/responses should be provided using JSON bodies.

`GET` methods do not require authentication of any kind.

`POST`/`PUT`/`DELETE` methods require authentication. Please refer to the
Authentication docs for further details.


## `GET` List

*URL:* `/api/v1/courses/`

A list of all the courses. Defaults to descending order based on the creation
date (newest courses first).

`GET` Parameters:

* `start`: An integer of the `id` to start at. Default is `null`.
* `limit`: A limit on how many results should be returned. Default is `100`.

Format:

    {
        "meta": {
            "start": <int>,
            "limit": <int>,
            "total": <int>,
            "prev": "<url-for-prev-page-of-results>"|null,
            "next": "<url-for-next-page-of-results>"|null,
        },
        "courses": [
            {
                "id": <int>,
                "title": "<title>",
                "system": "<system-name>",
                "course_type": "zerogravity|surface|srvrally|srvcross|stadium",
                "nearby_outfitting": "<string-description-of-nearest-station-or-port>",
                "distance_from_primary": "<decimal-in-Ls>",
                "distance_from_sol": "<decimal-in-Ly>",
                "notes": "<string-notes-about-course>",
                "course_info": {
                    // Common information:
                    "vehicle_type": "ship|srv",

                    // Specific information:
                    // Varies by course type, only **relevant** data present!

                    // For `zerogravity`:
                    "station_name": "<station-name>",
                    "number_of_rings": <int>,
                    "length": <int>,

                    // For `surface`:
                    "planet_name": "<planet-name>",
                    "coordinates": "<string-of-in-game-coordinates>",
                    "gravity": "<decimal>",

                    // For `srvrally`:
                    "planet_name": "<planet-name>",
                    "length": <int>,
                    "start_port_name": "<port-name>",
                    "end_port_name": "<port-name>",
                    "starting_line": "<optional-start-description>",
                    "finish_line": "<optional-end-description>",
                    "gravity": "<decimal>",
                    "planet_type": "rock|ice|lava|metallic|water|earth-like|ammonia|gas",

                    // For `srvcross`:
                    "planet_name": "<planet-name>",
                    "port_name": "<port-name>",
                    "gravity": "<decimal>",
                    "tidally_locked": <bool>,

                    // For `stadium`:
                    "planet_name": "<planet-name>",
                    "port_name": "<port-name>",
                    "gravity": "<decimal>",
                },
                "screenshots": [
                    "<url>",
                ],
                "created_by": "<CMDR-name>",
                "created": <int-timestamp-milliseconds-since-epoch>,
                "url": "<detail-url-on-elite-racing-site>"
            },
            // ...more entries..
        ]
    }

## `GET` Detail

*URL:* `/api/v1/courses/<int-id>/`

A detail of a single course.

`GET` Parameters:

* None

Format:

    {
        "id": <int>,
        "title": "<title>",
        "system": "<system-name>",
        "course_type": "zerogravity|surface|srvrally|srvcross|stadium",
        "nearby_outfitting": "<string-description-of-nearest-starport",
        "distance_from_primary": "<decimal-in-Ls>",
        "distance_from_sol": "<decimal-in-Ly>",
        "notes": "<string-notes-about-course>"
        "course_info": {
            // Common information:
            "vehicle_type": "ship|srv",

            // Specific information:
            // Varies by course type, only **relevant** data present!

            // For `zerogravity`:
            "station_name": "<station-name>",
            "number_of_rings": <int>,
            "length": <int>,

            // For `surface`:
            "planet_name": "<planet-name>",
            "coordinates": "<string-of-in-game-coordinates>",
            "gravity": "<decimal>",

            // For `srvrally`:
            "planet_name": "<planet-name>",
            "length": <int>,
            "start_port_name": "<port-name>",
            "end_port_name": "<port-name>",
            "starting_line": "<optional-start-description>",
            "finish_line": "<optional-end-description>",
            "gravity": "<decimal>",
            "planet_type": "rock|ice|lava|metallic|water|earth-like|ammonia|gas",

            // For `srvcross`:
            "planet_name": "<planet-name>",
            "port_name": "<port-name>",
            "gravity": "<decimal>",
            "tidally_locked": <bool>,

            // For `stadium`:
            "planet_name": "<planet-name>",
            "port_name": "<port-name>",
            "gravity": "<decimal>",
        },
        "screenshots": [
            "<url>",
        ],
        "created_by": "<CMDR-name>",
        "created": <int-timestamp-milliseconds-since-epoch>,
        "url": "<detail-url-on-elite-racing-site>"
    }