#!/usr/bin/python

import pypi
import sys

name = sys.argv[1]

package = pypi.pypackage(name)
package.extract()
package.make_specfile()
