from setuptools import setup, find_packages

setup( name='isr_meta',
       version='1.0',
       description='python meta package of the intelligent soft robotics laboratory',
       classifiers=[
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3',
       ],
       url='https://github.com/vincentberenz/lightargs.git',
       author='Vincent Berenz',
       author_email='vberenz@tuebingen.mpg.de',
       license='MIT',
       install_requires=['argcomplete',"colorama",
                         "treep","lightargs","fyplot",
                         "PySide2","roboball2d",
                         "matplotlib"],
       zip_safe=True
)



