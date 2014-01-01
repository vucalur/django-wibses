import os
from setuptools import find_packages, setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-wibses',
    version='1.0',
    packages=find_packages(where='django_wibses'),
    package_dir={'': 'django_wibses'},
    package_data={'': ['configs/*']},
    include_package_data=True,
    license='BSD License', # example license   TODO vucalur: LICENSE
    description='Web interface for building semantic scripts with lightweight Django backend.',
    long_description=README,
    url='http://www.example.com/',
    author='Wojciech Krzystek, Yaroslav Machkivskiy',
    author_email='see committer mails :-)',
    scripts=['scripts/wibses_runner.py'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)