#!/bin/bash
read -r -p "Host: " host
read -r -p "Port: " port
read -r -p "File: " file
id=$(curl -F "file=@$file" "http://$host:$port/upload")
echo "Image id: $id"