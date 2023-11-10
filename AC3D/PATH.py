import os

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
TEMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")

if not os.path.exists(DATA):
   os.makedirs(DATA)
if not os.path.exists(OUTPUT):
   os.makedirs(OUTPUT)
if not os.path.exists(TEMP):
   os.makedirs(TEMP)
