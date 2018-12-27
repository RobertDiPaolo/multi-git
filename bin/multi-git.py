#!/usr/bin/python3

# -*- coding: utf-8 -*-
import re
import sys

#find and append the multigit module path, must be a better way to handle this!
import imp
bt_path = imp.find_module('multigit')[1]
sys.path.append(bt_path)

from multigit.multigit import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())