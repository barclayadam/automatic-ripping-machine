#!/bin/bash
#trap "set +x; sleep 5; set -x" DEBUG

sudo groupadd arm
sudo useradd -m arm -g arm -G cdrom
#do sudo passwd arm when done with this installation

sudo apt-get install -y git
sudo add-apt-repository -y ppa:heyarje/makemkv-beta
sudo add-apt-repository -y ppa:stebbins/handbrake-releases
sudo add-apt-repository -y ppa:mc3man/bionic-prop

sudo debconf-set-selections <<< "postfix postfix/mailname string arm-env"
sudo debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"

sudo apt update -y
sudo apt install -y makemkv-bin makemkv-oss
sudo apt install -y handbrake-cli libavcodec-extra
sudo apt install -y abcde flac imagemagick glyrc cdparanoia
sudo apt install -y at
sudo apt install -y python3 python3-pip
sudo apt-get install -y libcurl4-openssl-dev libssl-dev  
sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install libdvd-pkg
sudo dpkg-reconfigure -f noninteractive libdvd-pkg
sudo apt install -y default-jre-headless

cd /opt
sudo mkdir arm
sudo chown arm:arm arm
sudo chmod 775 arm
sudo git clone -b emmakat https://github.com/emmakat/automatic-ripping-machine.git arm
sudo chown -R arm:arm arm
cd arm
# TODO: Remove below line before merging to master
sudo pip3 install -r requirements.txt 
sudo ln -sfn /opt/arm/setup/51-automedia.rules /lib/udev/rules.d/
sudo ln -sfn /opt/arm/setup/.abcde.conf /home/arm/
sudo cp docs/arm.yaml.sample arm.yaml
mkdir /etc/arm/
sudo ln -sfn /opt/arm/arm.yaml /etc/arm/
cd /home/arm
sudo mkdir .MakeMKV
cd .MakeMKV
sudo cp docs/settings.conf settings.conf
sudo apt autoremove
