import sys
import time

def Progress_Bar(Total, Progress, BarLength=20, ProgressIcon="#", BarIcon="-"):
    try:
        if BarLength <1:
            BarLength = 20
        Status = ""
        Progress = float(Progress) / float(Total)
        if Progress >= 1.:
            Progress = 1
            Status = "\r\n" 
        Block = int(round(BarLength * Progress))
        Bar = "[{}] {:.0f}% {}".format(ProgressIcon * Block + BarIcon * (BarLength - Block), round(Progress * 100, 0), Status)
        return Bar
    except:
        return "ERROR"


def Show_Bar(Bar):
    sys.stdout.write(Bar)
    sys.stdout.flush()
