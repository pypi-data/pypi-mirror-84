#!/bin/bash

stubgen coperator
cp out/coperator/myoperator.pyi coperator
cp out/coperator/myoperator.pyi monad
cp out/coperator/__init__.pyi coperator
touch coperator/py.typed
rm -r out
python3 setup.py sdist bdist_wheel
pip3 install dist/coperator-1.1.2-py3-none-any.whl
rm -r build 
rm -r coperator.egg-info
rm -r dist
