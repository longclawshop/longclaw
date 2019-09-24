set -o errexit
set -o pipefail
set -o nounset
shopt -s failglob
set -o xtrace

export DEBIAN_FRONTEND=noninteractive

function run_user_command {
    echo ''
    echo "RUNNING COMMAND: $1"
    tmpfile=$(sudo -u vagrant mktemp /tmp/run_user_command.XXXXXX)
    su - vagrant -c "$1; echo \\$? > $tmpfile"
    RETVAL=`cat $tmpfile`
    rm "$tmpfile"
    (( RETVAL )) && { echo "COMMAND RETURNED NON-ZERO EXIT CODE $RETVAL"; exit $RETVAL; }
    (( RETVAL )) || echo "COMMAND SUCCESS"
    echo ''
}

add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y build-essential libssl-dev tox python3.5 python3.6 python3.7

run_user_command "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash"
run_user_command ". /home/vagrant/.nvm/nvm.sh; nvm install stable"
run_user_command ". /home/vagrant/.nvm/nvm.sh; nvm use stable"
