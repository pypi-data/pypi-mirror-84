import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='bentoutils',
    version='0.0.7',
    author='Mark Moloney',
    author_email='m4rkmo@gmail.com',
    description='Utilities for working with BentoML',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/markmo/bentoutils',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'BentoML==0.9.2',
        'click==7.1.2',
        'docker==4.3.1',
        'emoji',
        'Jinja2==2.11.2',
        'kubernetes==11.0.0',
        'mysqlclient',
        'nmslib',
        'numpy',
        'PyYAML==5.3.1',
        'scikit-learn==0.23.2',
        'scipy',
        'simpletransformers==0.28.2',
        'spacy',
        'stringcase==1.2.0',
        'tensorflow==2.0.0',
        'text-unidecode',
        'stringcase==1.2.0',
        'tokenizers==0.7.0',
        'transformers==2.10.0',
        # '-f https://download.pytorch.org/whl/torch_stable.html',
        # 'torch==1.6.0+cpu',
        # 'torchvision==0.7.0+cpu',
    ],
    # dependency_links=[
    #     'https://download.pytorch.org/whl/torch_stable.html',
    # ],
    entry_points='''
        [console_scripts]
        bentopack=bentoutils.cli:pack
        deploy_to_knative=bentoutils.cli:deploy_to_knative
    ''',
    python_requires='>=3.6',
)
