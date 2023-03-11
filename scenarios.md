# Pet store test scenarios

## Performance criteria

We have not received any performance requirements for the Pet Store app.
So we chose the following metrics for each scenario, based on the analysis of the expected number of users:

1. Run parameters:
   - Users number: **200**
   - Spawn rate: **5**
   - Run time: **600s**

2. Failure criteria of the specific request
    - Execution time more than 1 second
    - Expected response code differs from the actual one

3. Failure criteria of the test run (process_exit_code=1)
    - Part of failed tasks is more than 2%
    - Average response time of requests is more than 500 milliseconds 

## Scenarios

1. Smoke test for performance. Calling some of the most frequently used endpoints. 
Locust file: `tests/smoke_load_test.py`
2. Performance test for pet management scenario. 
Locust file: `tests/pet_management_test.py`. 
Actions are performed in the following order:
- creating new pet
- getting all pets with status equal to one set during create
- getting created pet
- updating pet
- getting all pets with status equal to one set during update
- getting updated pet
- deleting pet