from setuptools import setup


setup(
    name='Flask-Alfred-DB',
    version='0.1.dev',
    license='ISC',
    description='An extension to integrate alfred-db with Flask apps.',
    url='https://github.com/alfredhq/flask-alfred-db',
    author='Alfred Developers',
    author_email='team@alfredhq.com',
    py_modules=['flask_alfred_db'],
    install_requires=[
        'Flask',
        'alfred-db',
    ],
)
