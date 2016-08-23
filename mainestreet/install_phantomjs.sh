#!/usr/bin/env bash
apt-get update
apt-get install build-essential chrpath libssl-dev libxft-dev -y
apt-get install libfreetype6 libfreetype6-dev -y
apt-get install libfontconfig1 libfontconfig1-dev -y

cd ~
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2
tar xvjf phantomjs-1.9.8-linux-x86_64.tar.bz2

mv phantomjs-1.9.8-linux-x86_64 /usr/local/share
ln -sf /usr/local/share/phantomjs-1.9.8-linux-x86_64/bin/phantomjs /usr/local/bin