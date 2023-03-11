from setuptools import setup

setup(
    name = "hey-gpt",
    version = "1.0.0",
    author = "Lennard Voogdt",
    author_email = "lennard@spring.nl",
    description = ("Use OpenAI/ChatGPT gpt-3.5-turbo on the command-line"),
    license = "MIT",
    keywords = "openai, chatgpt, ask, commandline, cli",
    url = "https://github.com/lennardv2/hey-gpt-cli",
    packages=['hey'],
    include_package_data=True,
    install_requires=['prompt_toolkit', 'tiktoken', 'colorama', 'pyyaml', 'openai', 'distro', 'termcolor'],
    entry_points={
        'console_scripts': [
            'hey = hey:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
    ],
)