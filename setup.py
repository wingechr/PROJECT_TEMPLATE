from setuptools import find_packages, setup

if __name__ == "__main__":

    with open("README.md", encoding="utf-8") as file:
        long_description = file.read()

    setup(
        packages=find_packages(),
        keywords=[],
        install_requires=[],
        name="PROJECT_TEMPLATE",
        description="DESCRIPTION",
        long_description=long_description,
        long_description_content_type="text/markdown",
        version="0.0.0",
        author="Christian Winger",
        author_email="c@wingechr.de",
        url="https://github.com/wingechr/PROJECT_TEMPLATE",
        download_url="https://github.com/wingechr/PROJECT_TEMPLATE",
        platforms=["any"],
        license="Public Domain",
        project_urls={"Bug Tracker": "https://github.com/wingechr/PROJECT_TEMPLATE"},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
            "Operating System :: OS Independent",
        ],
        entry_points={"console_scripts": ["project-cmd = MODULE.__main__:main"]},
        package_data={"test": ["data/**"]},
    )
