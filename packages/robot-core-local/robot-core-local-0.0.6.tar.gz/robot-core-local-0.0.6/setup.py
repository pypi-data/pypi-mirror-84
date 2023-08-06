from setuptools import setup, find_packages

setup(
    name='robot-core-local',
    version='0.0.6',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'imutils',
        'pip'
    ],
    entry_points={
        'console_scripts': [
            'robot_boot=robot_core.main:run'
        ]
    }
)