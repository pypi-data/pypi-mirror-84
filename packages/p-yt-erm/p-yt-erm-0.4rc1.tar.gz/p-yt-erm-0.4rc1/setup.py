import setuptools

with open("readme.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='p-yt-erm',
    version='0.4rc1',
    scripts=['pYTerm'],
    author='Anne & Lynice',
    maintainer='Alex Technically',
    maintainer_email='alexa@nicolor.tech',
    description='Easy to use youtube music streamer command line tool written in python3',
    long_description=long_description,
    long_description_content_type='text/plain',
    packages=setuptools.find_packages(),
    url='https://gitlab.com/mocchapi/pyterminal/',
    install_requires=[
        'python-vlc',
        'pafy',
        'beautifulsoup4',
        'youtube-dl',
        'pypresence',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Development Status :: 4 - Beta",
    ],
)
