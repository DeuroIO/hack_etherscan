# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from crawl import get_transcripts_at_p
import datetime
before_time = datetime.datetime.now()
print(get_transcripts_at_p("0x","0xe41d2489571d322189246dafa5ebde1f4699f498","15"))
first_query_time = datetime.datetime.now()

print(get_transcripts_at_p("0x","0xe41d2489571d322189246dafa5ebde1f4699f498","16"))
second_query_time = datetime.datetime.now()

print("first_query_time:{}".format(first_query_time-before_time))
print("second_query_time:{}".format(second_query_time-first_query_time))
