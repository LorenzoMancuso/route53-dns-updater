import boto3
import logging
import os
import requests


class UnconfiguredEnvironment(Exception):
    pass


LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)
HOSTED_ZONE_ID = os.getenv("HOSTED_ZONE_ID")
if not HOSTED_ZONE_ID:
    raise UnconfiguredEnvironment("Missing HOSTED_ZONE_ID environment variable")
RECORD_NAME = os.getenv("RECORD_NAME")
if not RECORD_NAME:
    raise UnconfiguredEnvironment("Missing RECORD_NAME environment variable")

if __name__ == "__main__":
    actual_ip = requests.get("https://checkip.amazonaws.com").text.strip()
    logging.debug("Detected public IP: ", actual_ip)

    client = boto3.client("route53")
    response = client.list_resource_record_sets(HostedZoneId=HOSTED_ZONE_ID)

    recordset = next(
        filter(
            lambda x: x.get("Name", "") == f"{RECORD_NAME}.",
            response.get("ResourceRecordSets"),
        ),
        None,
    )
    records = recordset.get("ResourceRecords", []) if recordset else None
    record = records[0] if records else None
    logging.debug("record: ", record)
    previous_ip = record.get("Value", None) if record else None

    if actual_ip != previous_ip:
        logging.info(f"Public IP change detected: {previous_ip}->{actual_ip}")
        response = client.change_resource_record_sets(
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": f"{RECORD_NAME}.",
                            "ResourceRecords": [
                                {
                                    "Value": actual_ip,
                                },
                            ],
                            "Type": "A",
                            "TTL": 300,
                        },
                    },
                ],
            },
            HostedZoneId=HOSTED_ZONE_ID,
        )
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode", None) == 200:
            logging.info("Public IP successfully updated")
        else:
            logging.error(f"Error performing the update: {response}")
    else:
        logging.info(f"Public IP hasn't changed: {previous_ip}")
