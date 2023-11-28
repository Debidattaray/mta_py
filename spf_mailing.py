"""
This for the the spf mailing.
use this after the normal configuration
"""

import go_module
import change_names

spf_domain = change_names.domainname
rdns_domain = change_names.domainname
ip_address = change_names.ip_address
rdns_record_name = change_names.rdns_record_name
sub_domain = change_names.sub_domain
full_domain = sub_domain + "." + spf_domain 

#spf
spf_record_type = 'TXT'
spf_record_name = sub_domain
spf_record_data = f'v=spf1 a mx ip4:{ip_address} ~all'

go_module.add_record(spf_domain, spf_record_type, spf_record_name, spf_record_data)


#DMRC
dmarc_record_type = 'TXT'
dmarc_record_name = '_dmarc.' + sub_domain
dmarc_record_data = f'v=DMARC1; p=none; sp=none; aspf=r; ruf=mailto:rua@{full_domain}; rua=mailto:ruf@{full_domain};'

go_module.add_record(spf_domain, dmarc_record_type, dmarc_record_name, dmarc_record_data)

"""
rdns_record_type = 'A'
rdns_record_name = rdns_record_name
rdns_record_data = ip_address

go_module.add_record(spf_domain, rdns_record_type, rdns_record_name, rdns_record_data)
"""
#Sub-Domain
sub_domain_record_type = 'A'
sub_domain_record_name = sub_domain
sub_domain_record_data = ip_address

go_module.update_or_add_record(spf_domain, sub_domain_record_type, sub_domain_record_name, sub_domain_record_data)

import OpenSSL

dkim_record_type = 'TXT'
dkim_record_name = 'cast._domainkey.'+sub_domain
print("=====dkim start===")
private_key = OpenSSL.crypto.PKey()
private_key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
dkim_path = f'/etc/pmta/dkim/cast.{full_domain}.pem'
with open(dkim_path, 'wb') as f:
  f.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, private_key))

# Extract the public key from the private key
public_key = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, private_key)
# Format the public key as a single line string
public_key = public_key.decode().replace('-----BEGIN PUBLIC KEY-----\n', '').replace('-----END PUBLIC KEY-----\n', '').replace('\n', '')
dkim_record = f'v=DKIM1; k=rsa; p={public_key}'
dkim_record_data = dkim_record

#with open('/etc/pmta/dkim/', 'w') as f:
#  f.write(dkim_record)
print('DKIM public key = ',dkim_record_data)

go_module.add_record(spf_domain, dkim_record_type, dkim_record_name, dkim_record_data)

##############################################################################################################################




with open("/etc/pmta/config", "r") as f:
    contents = f.readlines()

# Insert the new line at the 192nd index
contents.insert(185, f"domain-key cast,{full_domain}, {dkim_path} \n")

# Open the file in write mode and write the modified list to the file
with open("/etc/pmta/config", "w") as f:
    f.writelines(contents)








# Mx record 
# mx_record_type = 'MX'
# mx_record_name = '@'
# mx_record_data = [{'priority': 10, 'data': 'ASPMX.L.GOOGLE.COM'},\
#                           {'priority': 50, 'data': 'ASPMX3.GOOGLEMAIL.COM'}]

# update_or_add_record(domain, mx_record_type, mx_record_name, mx_record_data)

# client.add_record(domain, {'data': ip_address, 'name': 'abcd', 'ttl': 3600, 'type': 'A'})
