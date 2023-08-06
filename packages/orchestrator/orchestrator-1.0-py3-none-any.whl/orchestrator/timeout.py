#!/usr/bin/python3

'''
    Shared file
    
    timeout
    
    version: 1.0.0
'''

import time


class Timeout:
    def __init__(self, timeout_sec=0.0, expired=False):
        self.timeout_sec_ = timeout_sec
        self.expired_ = expired or timeout_sec==0.0
        if not self.expired_:
            self.t1_ = time.perf_counter()

    def expire(self):
        self.expired_ = True

    def is_expired(self):
        return self.remain_sec() == 0.0

    def remain_sec(self):
        if self.expired_:
            return 0.0
        passed_sec = time.perf_counter() - self.t1_
        if passed_sec >= self.timeout_sec_:
            self.expired_ = True
            return 0.0
        else:
            return self.timeout_sec_ - passed_sec

    def start(self, timeout_sec=None):
        if timeout_sec is not None:
            self.timeout_sec_ = timeout_sec
        self.expired_ = self.timeout_sec_ <= 0.0
        if not self.expired_:
            self.t1_ = time.perf_counter()
