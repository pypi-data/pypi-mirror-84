from setuptools import setup, find_packages

setup( name='isr_debian',
       version='0.02',
       description='creating a debian for isr code base',
       classifiers=[
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3',
       ],
       url='https://github.com/intelligent-soft-robots',
       author='Vincent Berenz',
       author_email='vberenz@tuebingen.mpg.de',
       license='MIT',
       packages=['isr_debian'],
       install_requires=['lightargs'],
       zip_safe=True,
       scripts=['bin/isr_make_debian']
)
