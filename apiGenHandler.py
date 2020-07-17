import threading

import json
from utils import generate_api_key
import random
from sortedcontainers import SortedSet, SortedKeyList
from datetime import datetime, timedelta


class apiGenHandler:
    """Class represents API key handler"""

    keys = {}
    active_count = 0
    blocked_queue = SortedKeyList([], key=lambda value: value["ts"].time())
    active_set = SortedSet([])

    def __init__(self):
        pass

    def gen_api_key(self):
        """Function to return a unique API key

        Time Complexity: O(log(n)) - n is the number of keys
        Return: True if it is successful else None
        """
        ret = None
        try:
            api_key = generate_api_key()
            self.keys[api_key] = {}
            self.keys[api_key]["state"] = 1
            self.keys[api_key]["ts"] = ''
            c = self.active_count
            c = c + 1
            self.active_count = c
            self.active_set.add(api_key)
            ret = True
        except Exception as e:
            print(e)
            ret = False
            pass
        return ret

    def get_available_api_key(self):
        """Function to return unblocked key

        Time Complexity: O(log(n)) - n is the number of keys
        Return: API Key if it is successful else None
        """
        c = self.active_count
        if c == 0:
            return None
        c = c-1
        self.active_count = c
        ret = None
        try:
            ran_val = random.randint(0, c)
            api_key = self.active_set[ran_val]
            self.active_set.remove(api_key)
            self.keys[api_key]["state"] = 0
            time1 = datetime.now() + timedelta(minutes=5)
            self.keys[api_key]["ts"] = time1
            block_element = self.keys[api_key]
            self.blocked_queue.add(block_element)
            print(self.keys)
            ret = api_key
        except Exception as e:
            print(e)
            ret = None
            pass
        # start the job if not started
        size = len(self.blocked_queue)
        if size == 1:
            a = threading.Thread(target=self.kill_api,
                                 name='kill-thread', daemon=True)
            a.start()
        return ret

    def unblock_api_key(self, key):
        """Function to unblocked key

        Time Complexity: O(log(n)) - n is the number of keys
        Return: True Key if it is successful else None
        """
        ret = None
        try:
            if self.keys[key]["state"] == 1:
                return None
            self.keys[key]["state"] = 1
            c = self.active_count
            c = c + 1
            self.active_count = c
            self.active_set.add(key)
            ret = True
        except Exception as e:
            ret = None
            print(e)
            pass
        return ret

    def delete_api_key(self, key):
        """Function to delete an API key

        Time Complexity: O(log(n)) - n is the number of keys
        Return: True Key if it is successful else None
        """
        ret = None
        try:
            if self.keys[key]["state"] == 1:
                self.active_set.remove(key)
                c = self.active_count
                c = c - 1
                self.active_count = c
            self.keys.pop(key, None)
            ret = True
        except Exception as e:
            print(e)
            pass
        return ret

    def poll_api_key(self, key):
        """Function to poll to extend API Key expiry by 5 minutes

        Time Complexity: O(log(n)) - n is the number of keys
        Return: True Key if it is successful else None
        """
        try:
            time_stamp = self.keys[key]["ts"]
            ts = self.keys[key]["ts"]
            self.blocked_queue.remove(self.keys[key])
            ts = ts + timedelta(minutes=5)
            self.keys[key]["ts"] = ts
            self.blocked_queue.add(self.keys[key])
        except Exception as e:
            print(e)
            return None
        return True

    def kill_api(self):
        """Function run by a seperate thread delete expired API keys
        Once started this keeps running unless any interruption

        Time Complexity: O(log(n)) - n is the number of keys
        """
        while True:
            try:
                api_key = self.blocked_queue[0]
                ts = api_key["ts"].time()
                if ts < datetime.now().time():
                    self.blocked_queue.remove(api_key)
                    api_key["state"] = 1
                    self.active_set.add(api_key)
            except Exception as e:
                print(e)
                pass
