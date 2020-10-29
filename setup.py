from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="video-file-organizer",
    version="2",
    python_requires=">=3.6",
    description="""Organizes the video files in the correct directories""",
    long_description=readme(),
    url="https://github.com/Scheercuzy/video_file_organizer",
    author="MX",
    author_email="maxi730@gmail.com",
    license="MIT",
    install_requires=[
        "apscheduler==3.6.3",
        "babelfish==0.5.5",
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "filelock==3.0.12",
        "flask==1.1.2",
        "guessit==3.1.1",
        "itsdangerous==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "jinja2==2.11.2",
        "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pyaml==20.4.0",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2020.1",
        "pyyaml==5.3.1",
        "rebulk==2.0.1",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "sqlalchemy==1.3.20",
        "tzlocal==2.1",
        "uwsgi==2.0.19.1",
        "werkzeug==1.0.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
    ],
    dependency_links=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["vfo = video_file_organizer.__main__:main"]},
)
