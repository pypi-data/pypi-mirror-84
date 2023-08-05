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
- Some pages for every usertype
- Cookies for stateful operations

---

## Pipeline structure:
- **build**: get app's dependencies from [pip](https://pypi.org/project/pip/)
- **verify**: check static problems with [prospector](https://pypi.org/project/prospector/) and [bandit](https://pypi.org/project/bandit/)
- **unit-test**: run unit tests with [pytest](https://pypi.org/project/pytest/)
- **integration-test**: run integration tests with [pytest](https://pypi.org/project/pytest/)
- **package**: create a package with [setuptools](https://pypi.org/project/setuptools/) and [wheel](https://pypi.org/project/wheel/)
- **release**:
    - use [Gitlab's release API](https://docs.gitlab.com/ee/ci/yaml/#release) to create a new release on [GitLab's project page](https://gitlab.com/bicoccadisco/processo-e-sviluppo-del-software/2020_assignment1_flaskofcinema/-/releases)
    - use [twine](https://pypi.org/project/twine/) to release a new version to [pypi](https://pypi.org/)
- **deploy**: deploy on [Heroku](https://www.heroku.com/):
    - on every master push (staging version)
    - for every tagged version (release version)
- **documentation**: generate the PDF documentation for the project each time the README.md file is modified

## Pipeline features:
- Per job optimized cache
- Automatic generation of this documentation in a PDF format
- Directed Acyclic Graph structure using *needs*
- Diversified cache buckets

## Extra setup needed
- GitLab Runner on Docker
- Distributed cache using an S3 compatible bucket on docker to be able to run concurrent jobs with cache access
- Two Heroku dyno with postgresql add-on. One for each deploy version

---

## Deployed app available at:
- https://flaskofwater-staging.herokuapp.com/ (staging)
- https://flaskofwater-prod.herokuapp.com/ (releases)

---

## [Gitlab repository (private access)](https://gitlab.com/bicoccadisco/processo-e-sviluppo-del-software/2020_assignment1_flaskofcinema)

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
>- Run `pip3 install -r requirements.txt` with sufficient privilegies
>- Install your preferred BDMS and update the `DB_URI` in the .env file to connect to it
>
>## HOW TO RUN
>
>- Type `python -m flask run --port 9000 --no-debugger --no-reload` to run the app.
>- Open a local browser and go to `http://localhost:9000` to see the running app.
