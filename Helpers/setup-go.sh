curl -O https://storage.googleapis.com/golang/go1.11.2.linux-amd64.tar.gz
tar -xvf go1.11.2.linux-amd64.tar.gz
mv go /usr/local

cat << EOF >> ~/.bashrc
export GOPATH=$HOME/go
EOF
source ~/.bashrc
cat << EOF >> ~/.bashrc
export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
EOF
source ~/.bashrc