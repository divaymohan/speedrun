# speedrun

This project have functionality to setup events.

## Run this project
### Prerequisites
1. Docker Client
2. Docker-Compose

### Steps
1. Clone the repo:
    ```
   git clone https://github.com/divaymohan/speedrun.git
   ```
2. Open terminal in the project and change directory to `deploy`.
3. Run docker compose:
   ```
   docker-compose up --build
   ```
    You will see following screen:
![Screenshot 2025-02-16 at 3.29.38 PM.png](Screenshot%202025-02-16%20at%203.29.38%E2%80%AFPM.png)
4. Check if all the services are up and running on following urls
    1. PgAdmin on: http://localhost:5050/
    2. Redis-Commander on: http://localhost:8081/
    3. API-Service on: http://localhost:8000/api/docs#/
    4. Flower on: http://localhost:5556/workers

5. Now you can start hitting the apis on api-service.

Credentials:

1. For Api service:
   ```
   username: speedrun
   password: speedrun
   ```
2. For pg-admin:
   ```
   username: admin@speedrun.com
   password: speedrun
   ```
3. Add server to the pg-admin with following creds
    ```
    HostName: speedrun-db
    User Name: speedrun
    Password: speedrun
    Database: speedrun
    ```


APIS :

