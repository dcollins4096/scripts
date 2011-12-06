#!/usr/bin/env python
from datetime import *
import sys
for wall in sys.argv[1:]:
    round = int(float(wall))
    print datetime.fromtimestamp(round).isoformat()
#end
