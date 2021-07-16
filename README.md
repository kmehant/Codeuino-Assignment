# API Key handler
A simple python server written using Flask framework, to handle API keys as per 
requirements stated in the assignment document. I was able to achieve this in **O(lgn)** 😁

Code has doc strings and relevant comments explaining different modules

**Problem 2:** I have curated few implementation ideas for the Donut project. Here is the [Link](https://docs.google.com/document/d/1m5z3cI0M4NvnPgRABnV-bbk80kosjz6ZD7HwWwtKzSw/edit?usp=sharing)

<hr>

## What is in here 🤔
1. Design
   1. Data Structures
   2. Functions
2. Setup
3. API
4. Tests

## Design

`apiGenHandler` handler Class holds all the required functions and data. Spawning a server will create a single `apiGenHandler` object which holds the data until the lifetime of the server.

<hr>

### Data structures:

`keys` dictionary holds the below structure
```
keys: {
    "<api-key>": {
        "state": 0/1
        "ts": <datetime object>
    }
}
```
`state`: 0 for blocked and 1 for unblocked

`ts`: holds time as datetime object

`activity_count` variable will be incremented whenever a new API key is generated and decremented when API key is deleted or pushed to block state. This we can get the count of Unblocked API keys in O(1)

`blocked_queue` is a sorted set making most of its operations done in O(log(n)) instead of O(n). This sorted list holds the `"<api-key>"` objects which are in blocked state and sorted by the timestamps. This queue is used by the daemon thread `kill-thread` which continuously checks for the top element in the queue and removes them once the 5 minutes time is completed

`active_set` is also a sorted set which holds the set of active or available API keys. This DS has been choosed to optimize the random choosing operation which will be done in O(log(n)) which also includes the deletion of the element from the set.

<hr>

### Functions

`gen_api_key`
```
Time Complexity: O(log(n)) - n is the number of keys
Return: True if it is successful else None
```

Generates a random API key. I am using `urandom` module to generate a 32 Byte => 256 bit random value and converting that to a hexadecimal value. Utility function `generate_api_key` does the job. Adds the object to the `active_set` which will used to during random choosing in O(lgn) and increment `active_count` for getting the count in O(1). Sets the state of the API key in O(1).

`get_available_api_key`
```
Time Complexity: O(log(n)) - n is the number of keys
Return: API Key if it is successful else None
```
It checks for the `active_count` variable to get the number of available API keys in O(1). 
Later it decrements `active_count`. It chooses a random number between 0 and number of available API keys which we got earlier. We then access the API key from `active_set` in O(log(n)) and deletes the Key with the same complexity. Further we will change the state of the retrieved API key to 0 in O(1) and will find a datetime object adding 5 minutes to the present time to get the expiration time. Upon assigning the expiration time to `ts` key will add this object to the `block_queue` sorted set (where the sort is based on the time). We then spawn a thread `kill thread` which will keep on check the `blocked_queue` to delete the keys after the expiration. As the thread is set as a Daemon thread it does not block the main process. So we will simply return the API key. 

`unblock_api_key`
```
Time Complexity: O(log(n)) - n is the number of keys
Return: True Key if it is successful else None
```
We change the `state` key to 1 and increment the `active_count` and add the the key to the `active_set` in O(lg(n)) and return.

`delete_api_key`
```
Time Complexity: O(log(n)) - n is the number of keys
Return: True Key if it is successful else None
```
We delete the key irrespective of the `state`.

`poll_api_key`
```
Time Complexity: O(log(n)) - n is the number of keys
Return: True Key if it is successful else None
```
We change the `ts` key which is a datetime object by incrementing it with more 5 minutes. So here we will delete the previous key from the `blocked_queue` in O(lg(n)) and add it back in O(lg(n)) with new `ts` which will ultimately equivalent to pushing the key to the bottom of the queue.

`kill_api`
```
Time Complexity: O(log(n)) - n is the number of keys
```
This function is run by the Daemon thread `kill-thread` which will be in infinte loop of checking the `blocked_queue` sorted set. It is handled with Try and catch block so that it is always in the loop even there is a key error.

<hr>

## Setup

Clone the repository
```
$ git clone https://github.com/kmehant/Codeuino-Assignment.git
```

Install python modules
```
$ pip install -f requirements.txt
```

Start the server
```
$ export FLASK_APP=app.py
$ flask run
```

<hr>

## API

```
Request GET /

description:
To ping the server
```

```
Request POST /key

description:
To generate an API key
```

```
Request GET /key

description:
To get an available API key
```

```
Request DELETE /key/del/<apikey>

description:
To delete an API key
```


```
Request POST /key/unblock/<key>

description:
To unblock the given API key
```

```
Request POST /key/poll/<key>

description:
To poll to server for the given API key which extends expiry time by 5 minutes
```
Tests
```
pytest test.py
```
![](./Screenshot%202020-07-17%20at%208.10.22%20PM.png)

