import setuptools

setuptools.setup(
    name="dc-crawler",
    version="1.0.0",
    license='MIT',
    author="seunghyukcho",
    author_email="shhj1998@postech.ac.kr",
    description="한국 최대의 익명 커뮤니티, DCInside 의 크롤링을 도와주는 python library 입니다.",
    long_description=open('README.md').read(),
    url="https://github.com/seunghyukcho/dc-crawler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
