#!/bin/bash
read -r -p "Host: " host
read -r -p "Port: " port
read -r -p "ID: " id
read -r -p "Scale: " scale
curl "http://$host:$port/get/$id?scale=$scale" --output out.jpg