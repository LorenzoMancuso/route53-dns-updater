kubectl create secret generic route53-dns-updater-aws-credentials --dry-run=client --from-file=credentials=$HOME/.aws/credentials -o yaml | \
    kubeseal \
      --controller-name=sealed-secrets \
      --controller-namespace=default \
      --format yaml > route53-dns-updater-aws-credentials.yaml

kubectl create secret generic route53-dns-updater-aws-config --dry-run=client --from-file=config=$HOME/.aws/config -o yaml | \
    kubeseal \
      --controller-name=sealed-secrets \
      --controller-namespace=default \
      --format yaml > route53-dns-updater-aws-config.yaml