set -o errexit
set -o pipefail
set -o nounset
shopt -s failglob
set -o xtrace

export DEBIAN_FRONTEND=noninteractive

add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y tox python3.5 python3.6 python3.7
