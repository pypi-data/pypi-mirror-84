# python3 package manager is pip3, install it for the system.
sudo apt-get install python3-pip
# Will require the python mongo client library for interaction
sudo pip3 install pymongo
# Will use requests library for http and https
sudo pip3 install requests
# Need antlr runtime
pip install antlr4-python3-runtime
# Parsing HCL
pip install pyhcl==0.3.10
#install requirements
pip install -r requirements.txt

Mongo DB version used - 3.2.21 , can be upgraded to 3.4.18 or even ater 3.6.9. The latest current release is 4.0.4
mongoDB can be local or remote, you can control that from config.ini
Upgrade to 4.0.4 version and check the basic connections and query APIs.

TODO - Version selection and features involved.

cd $HOME/projects/upwork/liquware/whitekite
export PYTHONPATH=`pwd`:$PYTHONPATH
echo $PYTHONPATH
antlr4 -Dlanguage=Python3 comparator.g4

to start mongoDB at windows subsystem
screen -d -m mongod --config /etc/mongod.conf # start mongo server
screen -r # press ctrl+c to stop daemon


python3 validator.py container1

python3 validator.py container1 --db

cd <clone dir>
source <virtual env name>/bin/activate
# export PYTHONPATH=<clone dir>/src:<clone dir>/adv
export PYTHONPATH=<clone dir>/adv
echo $PYTHONPATH
export FRAMEWORKDIR=`pwd`
# py.test --cov=processor tests/processor --cov-report term-missing
py.test --cov=processor_enterprise tests/processor_enterprise --cov-report term-missing
Added WhiteKite-CI for pipeline tests.
