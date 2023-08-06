from distutils.core import setup, Extension

c_ext = Extension("bird_c",["bird_c.c"])

setup(
    name='voipkebird',
    version="0.0.1",
    ext_modules=[c_ext],
    install_requires=['none'],
    scripts=[
        'bin/bird.py'
    ]
)

