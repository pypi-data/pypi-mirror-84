from setuptools import setup, find_packages

setup(
    name="pluginable",
    version="0.1.0",
    description="Tiny but safe toolbox, for bringing a plugins system to your application.",
    author="williamfzc",
    author_email="fengzc@vip.qq.com",
    url="https://github.com/williamfzc/pluginable",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
)
