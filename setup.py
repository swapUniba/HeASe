from setuptools import setup, find_packages

setup(
    name='SustainaMeal',
    version='0.1.0',
    author='Giovanni Tempesta , Michele Ciro Di Carlo',
    author_email='info@tempestagiovanni.it , m.dicarlo6@studenti.uniba.it ',
    description='A library to suggest more sustainable or healthy alternative recipes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tuo-username/SustainaMeal',  # URL del repository GitHub
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'torch',

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Cambia se necessario
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',  # Assicurati che corrisponda alla versione Python che stai utilizzando
        'Programming Language :: Python :: 3.9',
        # Aggiungi altri classifier pertinenti
    ],
    python_requires='>=3.6',  # Specifica la versione minima di Python richiesta
    # Se la tua libreria contiene dati o altri file di tipo non-Python, usa questo parametro per includerli
    include_package_data=True,
    # Se hai dei script o dei comandi da installare insieme alla tua libreria, puoi specificarli qui
    entry_points={
        'console_scripts': [
            'my-command=SustainaMeal.module:main_function',  # Un esempio
        ],
    },
)