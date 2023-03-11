# Python Performance tests for Pet Store

# Before run the tests:
1. Install Python 3.6+
2. Install dependencies: pip install -r requirements.txt

## To run tests with UI:
1. Run the `locust -f <locust_file.py>` command
2. Open the http://localhost:8089/ in browser
3. Set the number of users and spawn rate and click "Start swarming"
4. Monitor stats on "Statistics", "Charts" etc. tabs

## To run tests without UI:
1. Configure number of users, spawn rate and run time in `locust.conf` file
2. Run the `locust -f <locust_file.py> --headless --html reports/report.html` command
3. Once testing finished, check stats in html report


## To run tests in docker-container's with UI
To increase the maximum possible server load created by your computer, use docker.
Because Python cannot fully utilize more than one core per process, you should typically run
one worker instance per processor core on the worker machines in order to utilize all their computing power.

1. Update locust file in `docker-compose.yml` for both: master and worker containers 
2. Run `docker build -t locust .` for building the base locust image
3. Run `docker-compose up --scale worker=n`, n - number of workers. 
4. Open the http://localhost:8089/ in browser 
5. Set the number of users and spawn rate and click "Start swarming"
6. Monitor stats on "Statistics", "Charts" etc. tabs

## To run tests in docker-container's without UI

1. Add `--headless` option for master service command in `docker-compose.yml`
2. Update locust file in docker-compose.yml for both: master and worker containers 
3. Configure number of users, spawn rate and run time in `locust.conf` file
4. Run `docker build -t locust .` for building the base locust image
5. Run `docker-compose up --scale worker=n`, n - number of workers. 
6. Once testing finished, check stats in `report_docker.html` file from `reports` directory
