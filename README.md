#HOWTO

Launch EC2 instance.
Locally:
source setup
ansible-playbook deploy.yml -u ubuntu

~~ansible-playbook deploy.yml -u username -i host_address, --ask-pass --ask-become-pass~~