import os
from setuptools import setup 
from setuptools import find_packages


setup(
        name = 'automation-api-server', 
        version = '1.0.0', 
        author = 'wf-automation', 
        description = ("contains the manager and the automation api server"), 
        license = 'BSD', 
        packages  = find_packages()
)
