from setuptools import find_packages, setup

setup(name="umaineapi",
      version = "0.1",
      description = "A collection of API's for various UMaine services",
      author = "Noah Howard",
      platforms = ["any"],
      license = "BSD",
      packages = find_packages(),
      install_requires = ["Flask", "requests", "flask-mysqldb", "jsonify" ],
      )