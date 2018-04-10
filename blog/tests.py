#!/usr/bin/env python
import rethinkdb as r

conn = r.connect()
conn.use('babyhome')

def x():
    return 'dry'
def y():
    return 'good'

class Chicken(object):
    weight = 1.1 #類別屬性

    def __init__(self):
        self.age = 18 #實例屬性(or 資料屬性)

    def get_age(self):
        return self.age


# Create your tests here.
