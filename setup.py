from distutils.core import setup, Extension
import sys
from glob import glob

sources = glob("src/*.c")
undefine = []
define = []

try:
    sys.argv.remove("--debug")
    undefine.append("NDEBUG")
    define.append(("DEBUG", 1))
except ValueError:
    pass

_core = Extension("posh._core",
                  sources,
                  define_macros=define,
                  undef_macros=undefine)

setup(name="posh",
      version="1.1",
      description="POSH -- Python Object Sharing",
      long_description="POSH -- Python Object Sharing",
      author="Steffen Viken Valvaag",
      author_email="steffenv@stud.cs.uit.no",
      maintainer="Steffen Viken Valvaag",
      maintainer_email="steffenv@stud.cs.uit.no",
      url="http://poshmodule.sourceforge.net/",
      license="GNU General Public License (GPL)",
      packages=["posh"],
      ext_modules=[_core])
