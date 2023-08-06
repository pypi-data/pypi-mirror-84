from setuptools import setup, find_packages

setup(
    name='Flask of Cinema',
    version='1.0.0',
    # long_description=__doc__,
    packages=find_packages(exclude=[".tests", ".tests.", "tests.", "tests"]),
    py_modules=["app", "db", "db_init"],
    include_package_data=True,
    zip_safe=False,
    description='A nice application. Really tho!',
    author='Alessandro Bernieri - 810104, Matteo Schizzerotto - 876362, Matteo Vergara - 874063',
    classifiers=[
      'Development Status :: 4 - Beta',
      'Framework :: Flask',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Education :: Testing'
    ],
    url='https://gitlab.com/bicoccadisco/processo-e-sviluppo-del-software/2020_assignment1_flaskofcinema',
    license='MIT',
    install_requires=[
      'Flask',
      'SQLAlchemy'
      'Flask-Login'
      'python-dotenv'
      'psycopg2-binary'
      'werkzeug'
   ]
)