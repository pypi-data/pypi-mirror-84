from setuptools import setup


setup(
    name='comports',
    version='0.1.0',
    url='https://github.com/zeevro/comports',
    download_url='https://github.com/zeevro/comports/archive/master.zip',
    author='Zeev Rotshtein',
    author_email='zeevro@gmail.com',
    maintainer='Zeev Rotshtein',
    maintainer_email='zeevro@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    license=None,
    description='A small GUI for launching PuTTY for COM ports',
    keywords=[
        'PuTTY',
        'COM',
        'serial',
        'GUI',
    ],
    zip_safe=True,
    packages=[
        'comports',
    ],
    install_requires=[
        'pyserial',
    ],
    entry_points=dict(
        gui_scripts=[
            'comports = comports.gui:main',
        ],
    ),
)
