"""
Asynchronous Request Library

This module re-implemented previous `scheduler` which relys on callback.
Methods in this version are written with asynchronous support of Python
language.
"""

from datetime import datetime

import requests


class AsyncRequestScheduler:
    """
    Scheduler of outcoming request
    """

    def __init__(self, request_interval):
        """
        Constructor

        params:
        request_interval        Time interval of requests(in ms)
        """
        self._request_interval = request_interval
        self._send_request_iter = self._send_request()
        next(self._send_request_iter)

    def _send_request(self):
        """
        Send request to remote server
        """
        last_request_time = None
        request_methods = {
            'GET': requests.get
        }
        ua = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/'
            '537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        next_request = yield
        url = next_request['url']
        method = next_request['method']
        params = next_request['params']
        while True:
            if last_request_time is not None:
                time_interval = (datetime.now() -
                                 last_request_time).microseconds
                if time_interval < self._request_interval:
                    continue
            last_request_time = datetime.now()
            next_request = yield request_methods[method](url, params,
                                                         headers=ua)
            url = next_request['url']
            method = next_request['method']
            params = next_request['params']

    def get(self, url, params=None):
        """
        Wrapper of get method

        parmas:
        url         URL
        parmas      Parameters of the request
        """
        return self._send_request_iter.send({
            'url': url,
            'method': 'GET',
            'params': params
        })