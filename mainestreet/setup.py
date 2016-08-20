from setuptools import find_packages, setup

setup(name="umaineapi_mainestreet",
      version = "0.1",
      description = "A service for scraping MaineStreet with an ID and password",
      author = "Noah Howard",
      platforms = ["any"],
      license = "BSD",
      packages = find_packages(),
      install_requires = ["requests", "flask-mysqldb", "jsonify", "selenium"],
      )
