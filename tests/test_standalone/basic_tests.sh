#!/bin/bash

set -e

gibberify --uninstall
gibberify --rebuild-dicts
gibberify -m 'test'
