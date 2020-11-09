# IOTA DR Uploader

an IOTA message uploader in Python3.7 for DR result

## Introduce

1. Check available nodes
2. Get DR data from database
3. Upload DR data to IOTA
4. Update database

### Files

+ [main.py](./main.py)
    main function for uploading DR data

+ [tangle.py](./uploader/tangle.py)
    implement IOTA node availability checker and message uploader

## Getting Started

### Prerequisites

- python 3.7
- Pipenv 2018.11.26

### Running Development

1. update the `.env` file
```sh
cp .env.sample .env
```

2. Installing Packages & Running
```sh
make init
make run
```

## Solved Problems

### package install error

+ pysha3
    + package: `pysha3` (dependency of pyota)
    + OS: Ubuntu 18.04
    + Error Message: `src/ccurlmodule.c:1:10: fatal error: Python.h: No such file or directory`
    + Reason: No `Python.h` file
    + Solution: Install python3.7-dev `$ apt-get install python3.7-dev`

# Contributer
Chi-Sung, Wang
