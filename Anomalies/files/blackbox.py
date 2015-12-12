#!/usr/bin/env python

import syslog
import random
import time
import math

events  = [
    (200, 0.78),
    (204, 0.09),
    (304, 0.09),
    (404, 0.03),
    (500, 0.005),
    (504, 0.005),
]

def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w

bcoef = 10
walks = [0,0]
coefs = [2,1]

def run():
    base = int(bcoef * math.sin(time.localtime().tm_hour))
    for i in range(len(walks)):
        u = random.random()
        if (u<= 0.5): walks[i]+=coefs[i]
        else:         walks[i]-=coefs[i]
        if (walks[i] < 0): walks[i] = 0
    value = base + sum(walks)
    for i in range(value):
        sleep = random.random()/100
        syslog.syslog("{:03d} event happened st={:f}".format(weighted_choice(events), sleep))
        #syslog.syslog("{:03d} event happened {:d} {:d} <> {:f}".format(weighted_choice(events), base, sum(walks), sleep))
        time.sleep(sleep) #sleep from 0 to 10 ms

while True:
    run()
