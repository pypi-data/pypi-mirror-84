from distutils.core import setup

setup(
    # Application name:
    name="axplus",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="yijie zeng",
    author_email="axplus@163.com",

    # Packages
    packages=["axplus"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/axplus/",

    #
    # license="LICENSE.txt",
    description="Reactive for server-side rendering",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "django>=2.2",
    ],
)
