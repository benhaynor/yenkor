#!/bin/sh
sed -e 's/$/ Z/' -e 's/ \([^ ]* *[^ ]\)/_\1/g' -e 's/[ ]*Z$//'
