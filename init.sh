#! /bin/bash
set -uex
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

echo 'decrypt .env file'
gcloud beta secrets versions access latest --secret=vt-etl-agent --project=voicetube-test > "${DIR}/.service_acount.json"
