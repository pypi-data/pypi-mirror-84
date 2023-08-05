from setuptools import setup

setup(
  name="joe-username",
  version="0.1.0",
  packages=["joe_username"],
  license="MIT",
  author="Shreyas",
  author_email="shreyas.sreenivasa@gmail.com",
  url="https://github.com/shreyas44/joe-username",
  description="Generate a bunch if words Joe says",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">3.6.0",
  entry_points={
    "console_scripts": [
      "joe-username = joe_username.__main__:main"
    ]
  }
)
