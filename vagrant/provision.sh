set -o errexit
set -o pipefail
set -o nounset
shopt -s failglob
set -o xtrace

export DEBIAN_FRONTEND=noninteractive

add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y build-essential libssl-dev tox python3.5 python3.6 python3.7

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
. $HOME/.nvm/nvm.sh
nvm install stable
nvm use stable
