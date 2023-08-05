import datetime
import ccalafiore as cc;
cc.initiate()

sec = cc.clock.SecTimer()

time = cc.clock.AllUnitTime(seconds=1000000)

delta = datetime.timedelta(seconds=1000000)

# timer = cc_clock.Timer()
d1= datetime.datetime.today()
d2 = datetime.datetime.today()
diff = d2 - d1
dddd