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
********
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
********

Tech Stack used in this project:
1. Python FastAPI to build apis.
2. Postgres database to store triggers and logs
3. Celery Worker to run triggered tasks
4. Celery Beat + RedBeatScheduler to schedule the tasks
5. Redis as broker
6. Flower to track the number of messages processed or failed
7. Redis Commander: To track the scheduled tasks.
8. Swagger as API docs
9. Aws Ec2 for simple hosting

Minimum required machine:
1. Ram: 4 GB
2. Hard Disk Memory: 8 GB
3. CPU: 2
4. Expected cost 30 USD for 1 month

Note:
1. Do not schedule more then 2 tasks, It can full memory, because everything is running on very minimum infra.
2. Please delete the trigger manually.

*********
### How to use APIs:
***********
#### Schedule Tasks with interval
**Step 1:** please create a trigger with payload:
```json
{
  "name": "Sample Scheduled",
  "trigger_type": "scheduled",
  "schedule_time": "2025-02-16T10:12:23.719Z",
  "schedule_interval": 5
}
```
Note: schedule_interval will be in seconds.

**Step 2:** Get all triggers

**Step 3:** Find id for the trigger created.

**Step 4:** Hit api to start the task.

**Step 5:** Monitor the event logs by trigger id

****************

#### Schedule Tasks without interval
**Step 1:** please create a trigger with payload:
```json
{
  "name": "Sample Scheduled",
  "trigger_type": "scheduled",
  "schedule_time": "2025-02-16T10:12:23.719Z"
}
```

**Step 2:** Get all triggers

**Step 3:** Find id for the trigger created.

**Step 4:** Hit api to start the task.

**Step 5:** Monitor the event logs by trigger id

********

#### API Tasks
**Step 1:** please create a trigger with payload:
```json
{
  "name": "Sample Scheduled",
  "trigger_type": "api",
  "schedule_time": "2025-02-16T10:12:23.719Z",
  "api_payload": {"name":  "divay", "email":  "divay@gmail.com"},
  "api_url": "http://localhost:8000/api/test"
}
```
Note: Please use same api given in the payload

**Step 2:** Get all triggers

**Step 3:** Find id for the trigger created.

**Step 4:** Hit api to start the task.

**Step 5:** Monitor the event logs by trigger id

*************

Thanks for giving this assignment. Leaner lot of new things.

Credits:
1. ChatGPT (Helped in solving bugs)
2. https://youtu.be/nj-kFI_UDC0?si=vxOC7p9-mOq164XX
3. https://youtu.be/mcX_4EvYka4?si=VhCh9FUEXBLoEVXo
4. https://youtu.be/iwxzilyxTbQ?si=lSDy3nKD_KWu9kbd
5. https://medium.com/@yogesh.bhattarai073/how-i-implemented-celery-beat-scheduling-in-fastapi-22b7ee832ea3
6. https://stackoverflow.com/questions/21827290/celery-beat-different-time-zone-per-task
