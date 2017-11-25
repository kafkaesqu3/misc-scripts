apt-get update
apt-get -y install git build-essential python2.7 python2.7-dev python-pip libssl1.1 libssl-dev
pip install --user pipenv
git clone https://github.com/byt3bl33d3r/CrackMapExec.git -b v3.1.5dev --recursive
python setup.py install
