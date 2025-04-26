from setuptools import setup, find_packages


install_requires = [
    "boto3>=1.33.13,<1.34.0",
    "jmespath>=1.0.1",
    "termcolor>=1.1.0,<2.0.0",
    "python-dateutil>=2.8.2",
]


setup(
    name="awslogs",
    version="1.0",
    url="",
    license="BSD",
    author="",
    author_email="",
    description="awslogs is a simple command line tool to read aws cloudwatch logs.",
    long_description="awslogs is a simple command line tool to read aws cloudwatch logs.",
    keywords="aws logs cloudwatch",
    packages=find_packages(exclude=['tests']),
    platforms="any",
    python_requires=">=3.7",
    install_requires=install_requires,
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "awslogs = awslogs.bin:main",
        ]
    },
    zip_safe=False,
)
