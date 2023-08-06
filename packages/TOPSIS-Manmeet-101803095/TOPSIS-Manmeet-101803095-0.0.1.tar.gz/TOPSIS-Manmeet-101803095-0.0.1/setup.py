from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
  name = 'TOPSIS-Manmeet-101803095',
  version = '0.0.1',
  description = 'Find the Topsis Score Easily as well as preciously - Multiple Criteria Decision Making!',
  py_modules = ["topsis"],
  package_dir = {'':'TOPSIS-Manmeet-101803095'},
  package_data={'':['LICENSE.txt']},
  include_package_data=True,
  url="https://github.com/manmeet-kaur18/Topsis",
  author="Manmeet Kaur",
  author_email="manmeetkaur18102000@gmail.com",
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  long_description=long_description,
  long_description_content_type="text/markdown",
  extras_require={
    "dev":[
        "pytest>=3.7",
    ],
  },
)
