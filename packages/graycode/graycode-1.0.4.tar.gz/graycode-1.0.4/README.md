# Introduction

Graycode library implements functions to convert gray code to two's complement
integer and vice versa.

See LICENSE.md for copyright information. This library is licensed under the
MIT license.

See https://en.wikipedia.org/wiki/Gray_code for details about gray codes.

# Installation

```
$ python3 setup.py install
```
Or from PyPi:
```
$ pip3 install graycode
```

# Example

    import graycode

    graycode.tc_to_gray_code(2)
    # => 3
    graycode.gray_code_to_tc(3)
    # => 2
