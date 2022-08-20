docker run -ti --rm \
    -e HOSTED_ZONE_ID=$1 \
    -e RECORD_NAME=$2 \
    -e LOG_LEVEL=${3:-INFO} \
    -v $HOME/.aws:/root/.aws:ro \
    route53-dns-updater
