# EC2 Linux 2

echo "$(uname -s)-$(uname -r)-$(uname -m) with glibc $(ldd --version | grep -o -m 1 '[0-9]\+\.[0-9]\+')"
# Linux-5.10.226-214.880.amzn2.x86_64-x86_64 with glibc 2.26

# [ec2-user@ip-172-31-39-5 ~]$ dot -V
# dot - graphviz version 2.30.1 (20180828.1746)

sudo yum install -y cmake
sudo yum groupinstall "Development Tools" -y
sudo yum install -y libtool expat-devel
sudo yum install python3-devel

# wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
# wget https://gitlab.com/graphviz/graphviz/-/package_files/6163716/download -O graphviz-2.46.0.gz
wget https://gitlab.com/graphviz/graphviz/-/archive/2.46.0/graphviz-2.46.0.tar.gz

tar -xvf graphviz-2.46.0.tar.gz
cd graphviz-2.46.0

# ./configure
# make

mkdir build
cd build
cmake ..
make