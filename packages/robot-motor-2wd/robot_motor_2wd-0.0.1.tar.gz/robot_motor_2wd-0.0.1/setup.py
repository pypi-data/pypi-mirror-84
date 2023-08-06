from setuptools import setup, find_packages

setup(
    name='robot_motor_2wd',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'RPi.GPIO'
    ],
    entry_points={
        'console_scripts': [
            'robot_motor_2wd=robot_motor_2wd.main:run'
        ]
    }
)
