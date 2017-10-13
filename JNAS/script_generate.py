#!/usr/bin/env python
# -*- coding: utf-8 -*-

fw = open("wav2list_script.txt","w")

for i in range(3):
    for j in range(1, 51):
        number = "{0:03d}".format(50*i+j)
        strmkdir_f = "mkdir /home/akiyama/JNAS/JNAS_voicedata/WAVES_DT/F" + number
        strmkdir_m = "mkdir /home/akiyama/JNAS/JNAS_voicedata/WAVES_DT/M" + number
        fw.write("\n%s"%strmkdir_f)
        fw.write("\n%s"%strmkdir_m)
    for k in range(1, 51):
        number = "{0:03d}".format(50*i+k)
        # strcd_f = "cd /home/akiyama/JNAS/JNAS" + str(i+1) + "/WAVES_DT/F" + number + "/NP"
        strls_f = "ls /home/akiyama/JNAS/JNAS1/WAVES_DT/F" + number +"/NP/*.wav | xargs -i basename {} | xargs -L 1 python pyworld_jnas" + str(i + 1) + ".py F" + number
        # fw.write("\n%s"%strcd_f)
        fw.write("\n%s"%strls_f)
        # strcd_m = "cd /home/akiyama/JNAS/JNAS" + str(i + 1) + "/WAVES_DT/M" + number + "/NP"
        strls_m = "ls /home/akiyama/JNAS/JNAS1/WAVES_DT/M" + number +"/NP/*.wav | xargs -i basename {} | xargs -L 1 python pyworld_jnas" + str(i + 1) + ".py M" + number
        # fw.write("\n%s" % strcd_m)
        fw.write("\n%s" % strls_m)

fw.close()