# libmake.py

A python library for implementing `makefile.py` scripts.

#### Non-goals

The goal of this package it's not:

- to provide any pre-built `Makefile`
- to deliver an alternative build-system for compiled languages

For the second one there is already `make`, and other tools specific for more
recent languages.

#### Instead...

`Makefile`'s logic it's useful for projects' tasks automation further than
compiling code, e.g.:

- compiling templates and contents
- define project's specific commands
  - useful also for collaboration (and to save working patterns anyhow)

## Usage

Define a `makefile.py` using building blocks provided, then run it as a script
with targets (so do `python makefile.py args...` in place of `make args...`).

See `tests/makefile.py` for an example makefile definition, and run `tests.py`
to show its output.
