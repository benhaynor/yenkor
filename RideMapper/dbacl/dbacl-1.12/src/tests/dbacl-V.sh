#!/bin/sh
# test dbacl -V switch
PATH=/bin:/usr/bin
DBACL=$TESTBIN/dbacl

test x"`$DBACL -V | head -1`" = x"dbacl version 1.12"
