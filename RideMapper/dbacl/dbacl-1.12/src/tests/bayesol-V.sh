#!/bin/sh
# test bayesol -V switch
PATH=/bin:/usr/bin
BAYESOL=$TESTBIN/bayesol

test x"`$BAYESOL -V | head -1`" = x"bayesol version 1.12"
