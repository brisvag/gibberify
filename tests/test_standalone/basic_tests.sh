#!/bin/bash

set -e

echo y | gibberify --uninstall
gibberify --rebuild-dicts
gibberify -m 'test'
