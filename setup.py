from setuptools import setup, find_packages

setup(
    name='SustainaMeal',
    version='0.1.0',
    author='Giovanni Tempesta , Michele Ciro Di Carlo',
    author_email='info@tempestagiovanni.it , m.dicarlo6@studenti.uniba.it ',
    description='A library to suggest more sustainable or healthy alternative recipes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GiovTemp/SustainaMeal.git',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'collection',
        'transformers',
        'torch',
        'scipy',

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'my-command=SustainaMeal.module:main_function',
        ],
    },
)