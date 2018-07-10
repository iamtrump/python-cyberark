from setuptools import setup

setup(name="cyberark",
  version="0.2",
  description="CyberArk API functions",
  url="https://github.com/iamtrump/python-cyberark",
  author="Mikhail Mironov",
  author_email="mikhailmironov@mikhailmironov.ru",
  license="MIT",
  packages=["cyberark"],
  install_requires=["requests"],
  zip_safe=False)
