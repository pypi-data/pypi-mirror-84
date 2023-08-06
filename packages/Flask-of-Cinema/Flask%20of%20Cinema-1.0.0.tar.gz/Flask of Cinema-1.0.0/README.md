# Create a DevOps pipeline for an existing Python-Flask project

## Members
- Alessandro Bernieri - 810104
- Matteo Schizzerotto - 876362
- Matteo Vergara - 874063

---

## App description
This is a simple Python web application to manage a cinema

- Libraries:
    - Flask
    - Flask-Login
    - SQL Alchemy
    - PostgreSQL
    - Materialize CSS
- Two user types:
    - admin
    - client
- Some pages for every user type
- Cookies for stateful operations

---

## Pipeline structure
- **build**: get app's dependencies from [pip](https://pypi.org/project/pip/)
- **verify**: check static problems with [prospector](https://pypi.org/project/prospector/) and [bandit](https://pypi.org/project/bandit/)
- **unit-test**: run unit tests with [pytest](https://pypi.org/project/pytest/)
- **integration-test**: run integration tests with [pytest](https://pypi.org/project/pytest/)
- **package**: create a package with [setuptools](https://pypi.org/project/setuptools/) and [wheel](https://pypi.org/project/wheel/)
- **release**:
    - use [Gitlab's release API](https://docs.gitlab.com/ee/ci/yaml/#release) to create a new release on [GitLab's project page](https://gitlab.com/bicoccadisco/processo-e-sviluppo-del-software/2020_assignment1_flaskofcinema/-/releases)
    - use [twine](https://pypi.org/project/twine/) to release a new version to [pypi](https://pypi.org/) at [https://pypi.org/project/Flask-of-Cinema/](https://pypi.org/project/Flask-of-Cinema/)
- **deploy**: deploy on [Heroku](https://www.heroku.com/):
    - on every master push (staging version)
    - for every tagged version (release version)
- **documentation**: generate the PDF documentation for the project each time the `README.md` file is modified

## Pipeline features
- Per job optimized cache
- Automatic generation of this documentation in a PDF format
- Directed Acyclic Graph structure using *needs*
- Diversified cache buckets
- Unit tests on single methods and unit test on combination of those + DB access.
- Releases on both Gitlab page and pypi
- Deploy on PaaS with Heroku

---

## Decisions made
- The build stage was made to install all project dependencies (test suite and deployments needs included) using pip and pypi repository.
- The verify stage uses prospector and bandit, as suggested, to check static errors and bad practices on the codebase.
- Unit and integration tests use the pytest suite that was choose as an easy way to test our Flask application.
- Package are managed with setuptools for the source code generation and wheel for binary generation.
- Release are created as equals on two different platforms. Pypi to have access to an easy installable package through pip and GitLab's releases to access binaries when browsing the repository.
- Deploy is executed on PaaS provider Heroku with two version of the app always available. One for the staging versions (master branch) and one for releases (tags).
- We initially made the pipeline extremely concurrent with many stages running at the same time. After some thoughts we preferred making it more sequential to reduce pipeline time in case of disruption.
- Documentation was initially generated manually after each update of the `README.md`. Now it's generated automatically from the pipeline itself each time we push an update to the repository.
- To reduce our dependence on GitLab's shared workers and their time limits we decided to host our own worker on Docker.


## Extra setup needed
- GitLab Runner on Docker
- Distributed cache using an S3 compatible bucket on docker to be able to run concurrent jobs with cache access
- Two Heroku dyno with PostgreSQL add-on. One for each deploy version

---

## Deployed app available at
- https://flaskofwater-staging.herokuapp.com/ (staging)
- https://flaskofwater-prod.herokuapp.com/ (releases)

---

## Git Repository 
[Gitlab (private access)](https://gitlab.com/bicoccadisco/processo-e-sviluppo-del-software/2020_assignment1_flaskofcinema)

---

### ***ORIGINAL README OF THE PROJECT***
>## HOW TO INSTALL
>
>***Simpler - w/ Docker***
>
>- Install [Docker](https://www.docker.com/) if necessary
>- Use Visual Studio Code and open the project using the [Remote - Containers](https://>marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) >extension
>- Visual Studio Code will download the Docker image and install all dependencies
>
>***Normal - w/o Docker***
>
>- Install [Python 3.7.x](https://www.python.org/downloads/) if necessary
>- Run `pip3 install -r requirements.txt` with sufficient privileges
>- Install your preferred BDMS and update the `DB_URI` in the .env file to connect to it
>
>## HOW TO RUN
>
>- Type `python -m flask run --port 9000 --no-debugger --no-reload` to run the app.
>- Open a local browser and go to `http://localhost:9000` to see the running app.
