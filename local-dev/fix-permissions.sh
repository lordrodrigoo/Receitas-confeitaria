#!/usr/bin/env bash


sudo chown -R $(id -u):$(id -g) static media
sudo chmod -R 777 static media

sudo chown -R $(id -u):$(id -g) db.sqlite3 media static
sudo chmod -R 777 db.sqlite3 media static

