from setuptools import setup, find_packages


setup(
    name='blackboxpackage',
    version='0.1.3',
    url='https://bitbucket.org/ainstec/black-box-package',
    license='MIT',
    author='Ravi Jose Fiori',
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author_email='ravi.fiori@concil.com.br',
    keywords='Pacote',
    description=u'Pacote de tratamento de dados',
    packages=find_packages(),
    #install_requires=['boto3==1.11.0', 'pandas==0.25.1', ' numpy==1.16.5', 'pyarrow==0.15.1', 'SQLAlchemy==1.3.15', 'psycopg2==2.8.4', 'psycopg2-binary==2.8.5', 'workalendar==10.4.0', 'cx-Oracle==8.0.1'],
)


# cria a pasta dist com o pacote
#python setup.py sdist bdist_wheel

# subir no ambiente de teste 
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# subir no pipy
#twine upload dist/*


#install
#pip3 install blackboxpackage==0.1.1

#from blackboxpackage.aws import S3
#from aws import S3
#from blackboxpackage import aws
#import blackboxpackage

#from distutils.core import setup

#setup( 
#    name='blackboxpackage', 
#    version= '0.1.2', 
##    ## TODO: be sure to change these next few lines to match your details!
#    packages=['blackboxpackage'],
#    py_modules=['blackboxpackage/aws', 'blackboxpackage/ftp', 'blackboxpackage/function', 'blackboxpackage/oracle', 'blackboxpackage/postgresql'],
#    author='Ravi Jose Fiori',
#    author_email='ravi.fiori@concil.com.br',
#    url='https://bitbucket.org/ainstec/black-box-package',
#    description='Pacote de tratamento de dados',
#    long_description='Test',
#    long_description_content_type="text/markdown",
#    license='MIT',
#)


#python setup.py sdist bdist_wininst 