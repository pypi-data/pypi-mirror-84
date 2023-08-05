from setuptools import setup, find_packages

setup(
    name='Flask of Cinema',
    version='0.9.3',
    # long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author='Alessandro Bernieri - 810104, Matteo Schizzerotto - 876362, Matteo Vergara - 874063',
    license='MIT',
    platform='web',
    install_requires=[
      'Flask',
      'SQLAlchemy'
      'Flask-Login'
      'python-dotenv'
      'psycopg2-binary'
      'werkzeug'
   ]
)