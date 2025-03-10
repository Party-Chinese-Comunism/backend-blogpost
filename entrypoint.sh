#!/bin/bash

# Iniciar o Filebeat em segundo plano
filebeat -e &

# Iniciar o Flask
flask run --host=0.0.0.0
