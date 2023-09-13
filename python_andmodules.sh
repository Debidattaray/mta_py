#yum install -y centos-release-scl

yum install -y python3
yum install -y python3-pip

#pip3 install setuptools-rust

pip3 install --upgrade pip
pip3 install pyopenssl
pip3 install GoDaddyPy



# Remove Pmta
systemctl stop pmta
rpm -e PowerMTA-4.5r1.rpm
yum remove -y PowerMTA*
rm -rf /etc/pmta /var/spool/pmta
systemctl stop postfix
yum remove postfix
echo "un-install completed"

# installation

yum -y install httpd
yum -y install screen wget
# screen -xR install
# cd /var/www/html
# wget https://abs.chinabistroindy.com/skr_pmta_setup.sh.tar
# #abs.chinabistroindy.com
# wget http://16.16.195.62/Sambit_LD.tar
# tar -xvf skr_pmta_setup.sh.tar
# tar -xvf Sambit_LD.tar
# sh skr_setup.sh
# systemctl restart httpd.service


service httpd restart
service mariadb restart
chmod 0777 /etc
chmod 0777 /etc/named.conf
chmod 0777 /var/named/*.fw.zone

cd /opt
yum -y install wget perl
wget http://51.81.210.15/PowerMTA/PowerMTA-4.0r6_64.rpm
wget http://51.81.210.15/PowerMTA/license
rpm -ivh PowerMTA-4.0r6_64.rpm

mv license /etc/pmta
rm -rf PowerMTA-4.0r6_64.rpm
cd /etc/pmta
mkdir log
mkdir files
mkdir dkim
cd /etc/pmta/dkim

echo "#########################################  STEP- 1  #######################################"



cd /etc/pmta/files
wget  http://54.144.205.201/PmtaConfig/dkim/f.tar.gz
wget  http://54.144.205.201/PmtaConfig/dkim/h.tar.gz
yum -y install tar
tar -xvf h.tar.gz
tar -xvf f.tar.gz
cd reports
sed -i 's/,$var,/$var/g' yesipcus.sh
sed -i 's/,$var,/$var/g' todipcus.sh
sed -i 's/,$var,/$var/g' ipcus.sh
cd /etc/pmta
echo "#########################################  STEP- 2  #######################################"
chmod 775 ./*
# python3 ./config_bash.py

ulimit -n 766889
service pmta restart
service pmtahttp restart
iptables -F
# https://tools.socketlabs.com/dkim/generator
echo "#########################################  STEP- 3  #######################################"

service pmta stop
python3 ./go_dns.py
#pmtad --debug
sh /apps/mta_py/clear_log.sh
echo "Auto log clean setup Done ... "
echo "#########################################  DNS Details  #######################################"

ulimit -n 766889
service pmta restart
service pmtahttp restart
echo "#########################################  If 2 ok Then Completed  #######################################"

