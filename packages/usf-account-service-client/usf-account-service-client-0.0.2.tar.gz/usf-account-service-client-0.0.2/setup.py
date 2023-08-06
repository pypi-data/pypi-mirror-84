from setuptools import find_packages
from setuptools import setup


def get_version():
    with open('version') as version_file:
        return version_file.read()


def get_requirements():
    with open('requirements.txt') as requirements_file:
        return [dependency.strip() for dependency in requirements_file if dependency.strip()]


setup(name='usf-account-service-client',
      version=get_version(),
      author="Ukuspeed",
      author_email="info@ukuspeed.gmail.com",
      description="Account service client",
      url="https://github.com/ukuspeed/usf-account-service",
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=get_requirements(),
      py_modules=['client']
      )
