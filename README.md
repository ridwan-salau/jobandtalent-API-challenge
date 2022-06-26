# Find Connected Devs on Twitter and GitHub
---
Find users on twitter that follow each other and are members of the same organization on GitHub. 

This project implements two endpoints that `/connected/realtime/dev1/dev2` `/connected/register/dev1/dev2` that return json resonses as follow:

- `/connected/realtime/dev1/dev2`: When provided two developer profiles, this endpoint returns whether the two developers mutually follow each other on Twitter and are members of the same organization(s) on GitHub and returns the following responses:

    - When not connected:

    ```JSON
    {
        "connected" : false
    }
    ```

    - When they are connected:

    ```JSON
    {
        "connected" : true
    }
    ```
    - The case they are connected:
    ```JSON
    {
        "connected" : true,
        "organisations": ["org1", "org2", "org3"]
    }
    ```

    - When there are errors:
    ```JSON
    {
        "errors": [
            "dev1 is no a valid user in github",
            "dev1 is no a valid user in twitter",
            "dev2 is no a valid user in twitter"
        ]
    }
    ```

- `/connected/register/dev1/dev2`: Return all status of a pair of developers from previous invocations of `/connected/realtime/dev1/dev2`:
```JSON
[
{
"registered_at" : "2019-09-13T09:30:00Z",
"connected" : false
},
{

"registered_at" : "2019-09-15T10:30:00Z",
"connected" : true,
"organisations": ["org1", "org2", "org3"]
},
{
"registered_at" : "2019-09-27T12:34:00Z",
"connected" : true,
"organisations": ["org1", "org2", "org3", "org4"]
}
]
```

## Technology Stack
- Flask-Restful for API
- SqlAlchemy + PostgreSQL for data storage and retrieval
- Docker and docker compose for deployment and infrastructure management
- Nginx as a reverse-proxy server
- Gunicorn as an application webserver

## How to Run Test

To test the application, run the following commang:

```docker compose -f docker-compose.test.yml up```

# How to Run Application

To run the application, run the following sets of command: first to build the images, then to run the containers:

```docker compose build```

```docker compose up```

# TO DOS

- Add test coverage for other parts of the code
- Document functions and modules
- Add type-hinting to function definitions
- Upload container image to Docker Registry
- Implement CI/CD with GitHub Actions to update image with latest
- Handle some http exceptions with Twitter and GitHub APIs