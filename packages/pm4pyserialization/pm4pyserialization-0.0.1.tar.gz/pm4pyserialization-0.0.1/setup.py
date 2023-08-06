from os.path import dirname, join

from setuptools import setup

import pm4pyserialization


def read_file(filename):
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


setup(
    name="pm4pyserialization",
    version=pm4pyserialization.__version__,
    description=pm4pyserialization.__doc__.strip(),
    long_description=read_file('README.md'),
    author=pm4pyserialization.__author__,
    author_email=pm4pyserialization.__author_email__,
    py_modules=[pm4pyserialization.__name__],
    include_package_data=True,
    packages=['pm4pyserialization', 'pm4pyserialization.objects', 'pm4pyserialization.objects.log',
              'pm4pyserialization.objects.log.exporter', 'pm4pyserialization.objects.log.exporter.parquet',
              'pm4pyserialization.objects.log.exporter.parquet.variants', 'pm4pyserialization.objects.log.importer',
              'pm4pyserialization.objects.log.importer.parquet',
              'pm4pyserialization.objects.log.importer.parquet.variants',
              'pm4pyserialization.objects.log.serialization', 'pm4pyserialization.objects.log.serialization.variants',
              'pm4pyserialization.objects.log.deserialization',
              'pm4pyserialization.objects.log.deserialization.variants'],
    url='http://www.pm4py.org',
    license='GPL 3.0',
    install_requires=[
        'pm4py>=2.0.0',
        'pyarrow>=1.0.1'
    ],
    project_urls={
        'Documentation': 'http://www.pm4py.org',
        'Source': 'https://github.com/pm4py/pm4py-source',
        'Tracker': 'https://github.com/pm4py/pm4py-source/issues',
    }
)
