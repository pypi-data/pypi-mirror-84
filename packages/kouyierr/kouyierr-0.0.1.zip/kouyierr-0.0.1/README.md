# kouyierr

![Kouyierr](logo.jpg)


## How to build

```bash
# create a virtual env
virtualenv venv

# activate virtual env 
source venv/bin/activate 

# run test and package
pip3 install .[test]
python3 setup.py test

# install snapshot build
pip3 install . --upgrade
```


## Releases

After a commit or merge on master [circleci](https://circleci.com/vmdude/kouyierr) deploys kouyierr automatically on [pypi](https://pypi.org/project/kouyierr/)

To install the release version

```bash
pip3 install --upgrade --user kouyierr
```
