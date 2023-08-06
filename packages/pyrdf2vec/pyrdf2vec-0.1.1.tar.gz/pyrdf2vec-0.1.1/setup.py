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
 'scikit-learn>=0.23.2,<0.24.0',
 'tomlkit>=0.7.0,<0.8.0',
 'tqdm>=4.48.2,<5.0.0']

setup_kwargs = {
    'name': 'pyrdf2vec',
    'version': '0.1.1',
    'description': 'Python implementation and extension of RDF2Vec',
    'long_description': '\n.. rdf2vec-begin\n\nWhat is RDF2Vec?\n----------------\n\nRDF2Vec is an unsupervised technique that builds further on\n`Word2Vec <https://en.wikipedia.org/wiki/Word2vec>`__, where an\nembedding is learned per word, in two ways:\n\n1. **the word based on its context**: Continuous Bag-of-Words (CBOW);\n2. **the context based on a word**: Skip-Gram (SG).\n\nTo create this embedding, RDF2Vec first creates "sentences" which can be\nfed to Word2Vec by extracting walks of a certain depth from a Knowledge\nGraph.\n\nThis repository contains an implementation of the algorithm in "RDF2Vec:\nRDF Graph Embeddings and Their Applications" by Petar Ristoski, Jessica\nRosati, Tommaso Di Noia, Renato De Leone, Heiko Paulheim\n(`[paper] <http://semantic-web-journal.net/content/rdf2vec-rdf-graph-embeddings-and-their-applications-0>`__\n`[original\ncode] <http://data.dws.informatik.uni-mannheim.de/rdf2vec/>`__).\n\n.. rdf2vec-end\n.. getting-started-begin\n\nGetting Started\n---------------\n\nInstallation\n~~~~~~~~~~~~\n\n``pyRDF2Vec`` can be installed in two ways:\n\n1. from `PyPI <https://pypi.org/project/pyrdf2vec>`__ using ``pip``:\n\n.. code:: bash\n\n   pip install pyRDF2vec\n\n2. from any compatible Python dependency manager (*e.g.,* ``poetry``):\n\n.. code:: bash\n\n   poetry add pyRDF2vec\n\nIntroduction\n~~~~~~~~~~~~\n\nTo create embeddings for a list of entities, there are two steps to do\nbeforehand:\n\n1. **create a Knowledge Graph object**;\n2. **define a walking strategy**.\n\nFor a more elaborate example, check at the\n`example.py <https://github.com/IBCNServices/pyRDF2Vec/blob/master/example.py>`__\nfile:\n\n.. code:: bash\n\n   PYTHONHASHSEED=42 python3 example.py\n\n**NOTE:** the ``PYTHONHASHSEED`` (*e.g.,* 42) is to ensure determinism.\n\nCreate a Knowledge Graph Object\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nTo create a Knowledge Graph object, you can initialize it in two ways.\n\n1. **from a file using RDFlib**:\n\n.. code:: python\n\n   from pyrdf2vec.graphs import KG\n\n   # Define the label predicates, all triples with these predicates\n   # will be excluded from the graph\n   label_predicates = ["http://dl-learner.org/carcinogenesis#isMutagenic"]\n   kg = KG(location="samples/mutag/mutag.owl", label_predicates=label_predicates)\n\n2. **from a server using SPARQL**:\n\n.. code:: python\n\n   from pyrdf2vec.graphs import KG\n\n   kg = KG(location="https://dbpedia.org/sparql", is_remote=True)\n\nDefine Walking Strategies With Their Sampling Strategy\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nAll supported walking strategies can be found on the\n`Wiki\npage <https://github.com/IBCNServices/pyRDF2Vec/wiki/Walking-Strategies>`__.\n\nAs the number of walks grows exponentially in function of the depth,\nexhaustively extracting all walks quickly becomes infeasible for larger\nKnowledge Graphs. In order to circumvent this issue, `sampling strategies\n<http://www.heikopaulheim.com/docs/wims2017.pdf>`__ can be applied. These will\nextract a fixed maximum number of walks per entity. The walks are sampled\naccording to a certain metric.\n\nFor example, if one wants to extract a maximum of 5 walks of depth 4 for each\nentity using the Random walking strategy and Uniform sampling strategy (**SEE:**\nthe `Wiki page\n<https://github.com/IBCNServices/pyRDF2Vec/wiki/Sampling-Strategies>`__ for\nother sampling strategies), the following code snippet can be used:\n\n.. code:: python\n\n   from pyrdf2vec.samplers import UniformSampler\n   from pyrdf2vec.walkers import RandomWalker\n\n   walkers = [RandomWalker(4, 5, UniformSampler())]\n\nCreate Embeddings\n~~~~~~~~~~~~~~~~~\n\nFinally, the creation of embeddings for a list of entities simply goes\nlike this:\n\n.. code:: python\n\n   from pyrdf2vec import RDF2VecTransformer\n\n   transformer = RDF2VecTransformer(walkers=[walkers], sg=1)\n   # Entities should be a list of URIs that can be found in the Knowledge Graph\n   embeddings = transformer.fit_transform(kg, entities)\n\n.. getting-started-end\n\nDocumentation\n-------------\n\nFor more information on how to use ``pyRDF2Vec``, `visit our online documentation\n<https://pyrdf2vec.readthedocs.io/en/latest/>`__ which is automatically updated\nwith the latest version of the ``master`` branch.\n\nFrom then on, you will be able to learn more about the use of the\nmodules as well as their functions available to you.\n\nContributions\n-------------\n\nYour help in the development of ``pyRDF2Vec`` is more than welcome. In order to\nbetter understand how you can help either through pull requests and/or issues,\nplease take a look at the `CONTRIBUTING\n<https://github.com/IBCNServices/pyRDF2Vec/blob/master/CONTRIBUTING.rst>`__\nfile.\n\nReferencing\n-----------\n\nIf you use ``pyRDF2Vec`` in a scholarly article, we would appreciate a\ncitation:\n\n.. code:: bibtex\n\n   @inproceedings{pyrdf2vec,\n     author       = {Gilles Vandewiele and Bram Steenwinckel and Terencio Agozzino\n                     and Michael Weyns and Pieter Bonte and Femke Ongenae\n                     and Filip De Turck},\n     title        = {{pyRDF2Vec: A python library for RDF2Vec}},\n     organization = {IDLab},\n     year         = {2020},\n     url          = {https://github.com/IBCNServices/pyRDF2Vec}\n   }\n',
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
