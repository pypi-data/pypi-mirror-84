[![GitHub tag](https://img.shields.io/github/tag/vmdude/kouyierr.svg)](https://github.com/vmdude/kouyierr/tags/)
[![GitHub license](https://img.shields.io/github/license/vmdude/kouyierr.svg)](https://github.com/vmdude/kouyierr/blob/main/LICENSE)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kouyierr.svg)](https://pypi.org/project/kouyierr/)
[![CircleCI](https://circleci.com/gh/vmdude/kouyierr.svg?style=shield&circle-token=bb402d38d6d34114914609699878802d86235c9a)](https://circleci.com/gh/vmdude/kouyierr)


![Kouyierr](logo.jpg)

This project is basically a document generator (Doc As Code) focused on a few targets like invoices, timesheet, resume or documentation.

The initial goal was to avoid using Microsoft Wo@#$ and Ex@#$ to generate these recurrent documents, and to be able to add a little automation (of course we're lazy ^^).


## Usage

This python module use `click` to facilitate cli calls, help is self-explanatory:

```
kouyierr --help
Usage: kouyierr [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  invoice
  version
```

We use [rich](https://github.com/willmcgugan/rich) Python module to add some fancy console display as well:

![richsample](rich_sample.png)

## Scope

With `click` module, we bundled several scope to make life easier

### invoice

This scope let you generate HTML/PDF invoice file based on YAML definition file and Jinja2 template.

```
kouyierr invoice generate --help
Usage: kouyierr invoice generate [OPTIONS]

  Generate a new invoice based on definition file and company template

Options:
  --year INTEGER                  Year of the invoice, default=current
  --month INTEGER                 Month of the invoice, default=current
  --company_config, --company TEXT
                                  Company config file  [required]
  --invoice_config, --invoice TEXT
                                  Invoice config file  [required]
  --template TEXT                 Template file path  [required]
  --help                          Show this message and exit.
```

It can be summoned simply like:

```bash
kouyierr invoice generate --company_config .data/invoice/myfancycompany.yml --invoice_config .data/invoice/nicecustomer.yml --template .data/invoice/myfancycompany.html.j2
```

Sample files can be found in this repo:
- [myfancycompany.html.j2](.data/invoice/myfancycompany.html.j2): Jinja2 template
- [myfancycompany.yml](.data/invoice/myfancycompany.yml): Company config file
- [nicecustomer.yml](.data/invoice/nicecustomer.yml): Invoice config file

Generated file with these sample can also be found in this repo:
- [202011_CUS.html](.data/invoice/202011_CUS.html): HTML file
- [202011_CUS.pdf](.data/invoice/202011_CUS.pdf): PDF file

### resume

TODO

### timesheet

TODO

## How to build

```bash
# create a virtual env
virtualenv venv

# activate virtual env 
source venv/bin/activate 

# run test and package
pip3 install .[test] --user --upgrade
python3 setup.py test

# install snapshot build
pip3 install . --user --upgrade
```


## Releases

After a commit or merge on master [circleci](https://circleci.com/vmdude/kouyierr) deploys kouyierr automatically on [pypi](https://pypi.org/project/kouyierr/)

To install the release version from PyPi:

```bash
pip3 install kouyierr --upgrade --user
```

Or you can install local version as well:

```bash
git clone git@github.com:vmdude/kouyierr.git && cd kouyierr
pip3 install . --upgrade --user
```


## License

This project is licensed under the MIT License (see the
`LICENSE` file for details).
