import os
from setuptools import setup
from setuptools import find_packages
from lds_merkle_proof_2019 import __version__

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

#with open('requires.txt') as f:
#    install_reqs = f.readlines()
#    reqs = [str(ir) for ir in install_reqs]

setup(
    name='lds-merkle-proof-2019-bloxberg',
    version=__version__,
    packages=find_packages(),
    #install_requires=reqs,
    url='https://github.com/crossoveranx/lds-merkle-proof-2019-py',
    license='MIT',
    author='bloxberg',
    install_requires=[          
          'py-multibase>=1.0.1',
          'cbor2>=4.1.2',
      ],
    author_email='info@bloxberg.org',
    description='MerkleProof2019 module for python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    download_url = 'https://github.com/crossoveranx/lds-merkle-proof-2019-py/archive/0.8.tar.gz'
)
