from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='replace_value_txt',  # Name library
    version='1.0.0',  # Version
    author='Bruno Nascimento',  # Name author
    author_email='bruno_freddy@hotmail.com',  # Author email
    long_description=long_description,  # Description read README.md
    long_description_content_type='text/markdown',  # Type description
    packages=['replace_value_txt'],
    url='https://github.com/BrunoASN/beaufort-scale',
    project_urls={
        'Código fonte': 'https://github.com/BrunoASNascimento/replace_value_txt',
        'Download': 'https://github.com/BrunoASNascimento/replace_value_txt/archive/main.zip'
    },
    license='MIT',  # License name
    keywords=['replace'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization'
    ],
    python_requires='>=3.6'
)
