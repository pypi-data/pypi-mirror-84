from distutils.core import setup

setup(
    name='easyMNIST',
    packages=['easyai'],
    version='0.0.1',
    license='MIT License',
    description='This package contains classes of pre-written Tensorflow models and functions '
                'to interact with them for students to play with and learn about the core high level concepts of AI.',
    author='Vincent Quirion',
    author_email='vincent.quirion@icloud.com',
    url='https://github.com/VincentQuirion/easyai',
    download_url='https://github.com/VincentQuirion/easyai/archive/v0.0.1.tar.gz',
    keywords=['ai', 'student', 'beginner', 'tensorflow', 'highschool', 'mnist'],
    install_requires=[
        'tensorflow',
        'numpy',
        'matplotlib',
        'opencv-python',
        'scipy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
    ],
)
