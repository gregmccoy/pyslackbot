from distutils.core import setup

setup(
    name="pyslackbot",
    version="0.2",
    license="MIT",
    description="a simple programable slackbot",
    author="Greg McCoy",
    author_email="gmccoy4242@gmail.com",
    url="https://github.com/gmccoy42/pyslackbot",
    requires=[
        'slackclient',
    ],
    packages = ['pyslackbot'],
)
