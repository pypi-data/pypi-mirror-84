import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="video_razor",
    packages=['video_razor'],
    version="0.0.3",
    license='MIT',
    author="David Alford",
    author_email="firstlast678@gmail.com",
    description="A package for slicing a video into N sections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/5starkarma/video-razor",
    download_url='https://github.com/5starkarma/video-razor/archive/0.0.3.tar.gz',
    keywords=['OPENCV', 'VIDEO', 'CUT', 'SLICE', 'RAZOR'],
    install_requires=[
        'numpy',
        'opencv-python',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
