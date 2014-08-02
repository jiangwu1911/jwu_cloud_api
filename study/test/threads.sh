#!/bin/sh

for i in $(seq 100)  ; do
    wget http://127.0.0.1:8080/hello --delete-after &
done
