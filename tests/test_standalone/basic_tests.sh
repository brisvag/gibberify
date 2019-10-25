#!/usr/bin/env bash

set -e

gibberify --help

gibberify --rebuild-dicts

gibberify -m 'test'
