# `mergyaml`
A command line tool to deep merge 1 to many yaml files and command line string
representations of a dict.  The merged result can be written to one of the
input files or a new file.

## Install
**Requirement:** Python 2.7
```console
pip install git+https://github.com/erkolson/mergeyaml
```

## Usage
```console
Usage: mergeyaml [OPTIONS]

Options:
  --version              Show the version and exit.
  -i, --input FILENAME   An input yaml file to merge.
  -f, --file FILENAME    A file to merge, also used to write output.
  -o, --output FILENAME  An output file to use for writing merged yaml.
  --set TEXT             A string representation of a dict to merge.
  --help                 Show this message and exit.```

Given `test.yaml`
```
web:
  replicas: 1
  image:
    tag: 1.0.3
    repository: erikolson/env-test
```
And `test2.yaml`
```
web:
  image:
    repository: erikolson/env-test-error
```

### Update a single value

Read a file, merge in a single dict string, write back to same file.

```console
mergeyaml --file test.yaml --set web.images.tag=1.0.4
```

`test.yaml` becomes:

```
web:
  replicas: 1
  image:
    tag: 1.0.4
    repository: erikolson/env-test
```

### Merge from several sources

Example merging two files and a dict string, output to a different file.

```console
mergeyaml --input test.yaml --input test2.yaml --set web.image.tag=1.0.4 --output=merged.yaml
```

Produces, `merged.yaml`:

```
web:
  replicas: 1
  image:
    tag: 1.0.4
    repository: erikolson/env-test-error
```
