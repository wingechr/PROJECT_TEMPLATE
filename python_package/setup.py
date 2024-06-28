from setuptools import setup

if __name__ == "__main__":
    setup(
        packages=["python_package"],
        keywords=[],
        install_requires=[],
        name="wingechr-PYTHON_PACKAGE",
        description="DESCRIPTION",
        long_description="",
        long_description_content_type="text/markdown",
        version="0.0.1",
        author="Christian Winger",
        author_email="c@wingechr.de",
        url="https://github.com/wingechr/PROJECT_TEMPLATE",
        platforms=["any"],
        license="CC0-1.0",
        project_urls={"Bug Tracker": "https://github.com/wingechr/PROJECT_TEMPLATE"},
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
            "Operating System :: OS Independent",
        ],
        package_data={"python_package": ["data/**"]},
        include_package_data=True,
    )
