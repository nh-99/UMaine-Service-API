from setuptools import find_packages, setup

setup(name="umaineapi_userserver",
      version = "0.1",
      description = "A service for storing authentication keys for all your services",
      author = "Noah Howard",
      platforms = ["any"],
      license = "BSD",
      packages = find_packages(),
      install_requires = ["flask", "requests", "flask-mysqldb", "flask-sqlalchemy", "flask-cors" ],
      )
