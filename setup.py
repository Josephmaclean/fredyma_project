from setuptools import setup

setup(
    name='Fredyma Studio Project',
    version='1.0',
    author='Joseph Maclean Arhin',
    author_email='josephmacleanarhin@outlook.com',
    description="An API for a studio management system for Fredyma",
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'Flask>=1.1.2',
        'Flask-SQLAlchemy>=2.4.1',
        'Flask-Migrate>=2.5.3',
        'psycopg2>=2.8.5'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python'
    ],
)
