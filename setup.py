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
        'psycopg2>=2.8.5',
        'python-dotenv>=0.12.0',
        'flask-marshmallow>=0.11.0',
        'marshmallow-sqlalchemy>=0.22.3',
        'PyJWT>=1.7.1',
        'twilio>=6.38.1',
        'blinker>=1.4',
        'sendgrid>=6.2.2'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python'
    ],
)
