#!/usr/bin/env python
# -*- coding: utf-8 -*-

fw = open("text2accphrase_script.txt","w")

for i in range(150):
    number = "{0:03d}".format(i+1)
    strmkdir = "mkdir /home/akiyama/JNAS/JNAS_scriptdata/" + number
    fw.write("\n%s" % strmkdir)

fw.close()