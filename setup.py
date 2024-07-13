from setuptools import setup, find_packages

setup(
    name='HeASe',
    version='0.1.0',
    description='A library to suggest more sustainable or healthy alternative recipes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where='sustainameal'),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'collection',
        'transformers',
        'torch',
        'scipy',
        'tqdm',
        'nltk',
        'openai==0.28',
        'langchain',
        'pydantic',
        'langchain_community'

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.7',
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'sustainameal=sustainameal.cli:main',
        ],
    },
)