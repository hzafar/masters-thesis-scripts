#!/bin/bash

## Usage: ./mkdot [output-directory]
## Run this from within the directory containing the dotfiles.

OUT=$1
for FILE in *.dot; do
  dot -Tpng $FILE -Kdot > $OUT/$FILE.png
done
