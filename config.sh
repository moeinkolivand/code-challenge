#!/bin/bash

source .env

export POSTGRES_USER=$DB_USER
export POSTGRES_DB=$DB_NAME
export POSTGRES_PASSWORD=$DB_PASSWORD

