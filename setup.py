from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Video File Organizer',
    version='2',
    python_requires='>=3.6',
    description="""Organizes the video files in the correct directories""",
    long_description=readme(),
    url='https://github.com/Scheercuzy/video_file_organizer',
    author='MX',
    author_email='maxi730@gmail.com',
    license='MIT',
    packages=['video_file_organizer'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vfo = video_file_organizer.__main__:main'
        ]
    },
)