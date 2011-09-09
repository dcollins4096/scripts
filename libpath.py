#!/usr/bin/env python

import os
import sys
if len( sys.argv ) > 1:
    ld_library_path_ugly = sys.argv[1]
else:
    ld_library_path_ugly = os.getenv('LD_LIBRARY_PATH')
ld_library_path_less_ugly = ld_library_path_ugly.split(':')
for path in ld_library_path_less_ugly:
    print path
#end
