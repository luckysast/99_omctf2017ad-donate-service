# -*- coding: UTF-8 -*-

import colorsys
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect

TOTAL_C = 100

connect('mongodb://omctf-mongo:27017/donations')
#connect('mongodb://localhost:27017/donations')

class KarmaDonation(MongoModel):
    value = fields.IntegerField(required=True)
    minimum = fields.IntegerField(required=True)
    maximum = fields.IntegerField(required=True)
    ddate = fields.DateTimeField(required=True)

def getHex():

    karma = KarmaDonation.objects.all().order_by([('ddate', -1)]).limit(1)
    if (karma.count() < 1):
        N = TOTAL_C-1
    else:
        karma = karma.first()
        N = int(TOTAL_C*(karma.value - karma.minimum)/(karma.maximum - karma.minimum + 1))

    HSV_tuples = [((x*120/TOTAL_C)/360., abs(x-50)/50., 0.7) for x in xrange(TOTAL_C)]

    rgb = HSV_tuples[N]
    rgb = map(lambda x: int(x*255), colorsys.hsv_to_rgb(*rgb))
    hex_out = ''.join(map(lambda x: chr(x).encode('hex'),rgb))
    return ('#'+hex_out)
