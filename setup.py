from setuptools import setup

setup(
    name="Happy Turtle",
    version="1.0",
    packages=["happy_turtle"],
    entry_points={
        'console_scripts': [
            'happy_turtle = happy_turtle_game:game_loop'
        ]
    },
    install_requires=[
        'pygame==2.5.2'
    ],
    author="Blandon Leung",
    description="A fun turtle jumping game",
    keywords="game pygame turtle",
    url="https://github.com/blaaaand/happy-turtle-game"
)
