# File Cryptor

## Install

    pip install fcryptor

## Usage
```fcryptor.py [-h] -i INPUT [-o OUTPUT] [-si StdIn] [-k KEY] [-c Crypt | -d Decrypt]```

```
optional arguments:
    -h, --help              show help message and exit
    -i , --input
                            Input File/stdin [for stdin pass -si | --stdin]
    -o , --output
                            Output crypt/decrypt result to File
    -si, --stdin            when stdin is true
    -k , --key              key of/for file
    -c , --crypt            crypting flag
    -d , --decrypt          decrypting flag
```