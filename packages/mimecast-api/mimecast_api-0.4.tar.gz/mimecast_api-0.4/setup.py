from setuptools import setup

with open("README.rst", encoding="utf-8") as readme_fp:
    readme_contents = readme_fp.read()

setup(
    name='mimecast_api',
    version='0.4',
    description='Access Mimecast email security services',
    long_description=readme_contents,
    long_description_content_type='text/x-rst',
    author='Jared Jennings',
    author_email='jjennings@fastmail.fm',
    url='https://gitlab.com/jaredjennings/python-mimecast_api',
    license='BSD-2-Clause',
    packages=['mimecast_api'],
    install_requires=['requests'],
    classifiers=[
    'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Email',
        'Topic :: Security',
        ],
)
