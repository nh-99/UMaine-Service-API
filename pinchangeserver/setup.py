from setuptools import find_packages, setup

setup(name="umaineapi_pinchangeserver",
      version = "0.1",
      description = "A service for connecting to myHousing using a Maine ID and ",
      author = "Noah Howard",
      platforms = ["any"],
      license = "BSD",
      packages = find_packages(),
      install_requires = ["requests", "flask-mysqldb", "jsonify", "mechanize", "beautifulsoup4", "html5lib" ],
      )
