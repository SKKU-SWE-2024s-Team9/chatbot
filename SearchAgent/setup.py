from setuptools import setup, find_packages

setup(
    name='SearchAgent',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openai',
        'langchain',
        'chromadb',
        'tiktoken',
        'langchain-openai',
        'langchain-community',
    ],
    entry_points={
        'console_scripts': [
            'search-agent=search_agent.__main__:main',
        ],
    },
)
