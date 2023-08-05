# joe-username
Generate a username with words directly from the Joe Dictionary

## Installation

`pip3 install joe-username` to install the CLI for the generator.

## Usage

### The CLI

```shell
# To generate a Joe username with 4 words.
$ joe-username 

# To generate a Joe username with 5 words.
$ joe-username 5 
```

### As a python module

```python
from joe_username import generate

# prints a joe username with 4 words from the joe dictionary
print(generate())

# prints a joe username with 5 words from the joe dictionary
print(generate(5))

```
