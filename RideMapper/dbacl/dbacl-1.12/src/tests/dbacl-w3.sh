#!/bin/sh
# test basic dbacl -l switch, trigrams
PATH=/bin:/usr/bin
DBACL=$TESTBIN/dbacl

prerequisite_command() {
    type $2 2>&1 > /dev/null
    if [ 0 -ne $? ]; then
        echo "$1: $2 not found, test will be skipped"
        exit 77
    fi
}

prerequisite_command $0 grep

DBACL_PATH="`pwd`/`basename $0 .sh`_`date +"%Y%m%dT%H%M%S"`"
export DBACL_PATH

mkdir "$DBACL_PATH"

echo "The quick brown fox jumped over the lazy dog" \
    | $DBACL -l dummy -w 3
head -3 "$DBACL_PATH/dummy" \
    | grep '# hash_size 15 features 24 unique_features 23 documents 0' \
    > /dev/null

RESULT=$?
rm -rf "$DBACL_PATH"

exit $RESULT