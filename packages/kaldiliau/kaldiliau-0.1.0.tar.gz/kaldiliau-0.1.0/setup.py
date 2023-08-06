
from distutils.core import setup

版本 = '0.1.0'

setup(
    name='kaldiliau',
    version=版本,
    author='ÌTHUÂNKHOKI',
    author_email='ithuan@ithuan.tw',
    url='https://ithuan.tw',
    packages=['kaldiliau'],
    package_dir={'kaldiliau': 'tsuan/kaldiliau'},
    description='Kaldi ê liāu.',
    keywords=[
        'Gí-im Piān-sik',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'TuiTse-TsuSin',
    ],
)
