# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrdf2vec',
 'pyrdf2vec.embedders',
 'pyrdf2vec.graphs',
 'pyrdf2vec.samplers',
 'pyrdf2vec.walkers']

package_data = \
{'': ['*']}

install_requires = \
['SPARQLWrapper>=1.8.5,<2.0.0',
 'attrs>=20.1.0,<21.0.0',
 'flask>=1.1.2,<2.0.0',
 'gensim>=3.8.3,<4.0.0',
 'matplotlib>=3.3.1,<4.0.0',
 'mimeparse>=0.1.3,<0.2.0',
 'networkx>=2.5,<3.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.1,<2.0.0',
 'python-louvain>=0.14,<0.15',
 'rdflib>=5.0.0,<6.0.0',
 'readme-renderer>=28.0,<29.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'tomlkit>=0.7.0,<0.8.0',
 'tqdm>=4.48.2,<5.0.0',
 'twine>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'pyrdf2vec',
    'version': '0.1.0',
    'description': 'Python implementation and extension of RDF2Vec',
    'long_description': None,
    'author': 'Gilles Vandewiele',
    'author_email': 'gilles.vandewiele@ugent.be',
    'maintainer': 'Gilles Vandewiele',
    'maintainer_email': 'gilles.vandewiele@ugent.be',
    'url': 'https://github.com/IBCNServices/pyRDF2Vec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
