rsync --recursive --exclude="*/node_modules/*" --exclude="*/.git/*" /vagrant /tmp

cd /tmp/vagrant

tox "$@"
