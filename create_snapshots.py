import boto3

# Creating client for EC2 service and passing the the AWS Access Key ID and AWS Secret Access Key as parameters
client = boto3.client('ec2', region_name='us-east-1', aws_access_key_id='', aws_secret_access_key='')

# Creating a dictionary with names of instances as the key and their volume ids as the value
volumes_dict = {
    'database-1': 'vol-0bd246509bb1ad386',
    'database-2': 'vol-0749649f64590da2e'
}

# Creating a dictionary of snapshots with their snapshot ids which were created successfully
successful_snapshots = dict()

# Iterate through each item in the volumes_dict and use key as the description of snapshot
for snapshot in volumes_dict:
    try:
        response = client.create_snapshot(
            Description = snapshot,
            VolumeId = volumes_dict[snapshot],
            DryRun = False
        )

        # Response is a dictionary containing ResponseMetadata and SnapshotId
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        snapshot_id = response['SnapshotId']

        # Checking if status_code was 200 or not to ensure that the snapshot was created successfully
        if status_code == 200:
            successful_snapshots[snapshot] = snapshot_id
    except Exception as e:
        exception_message = "There was an error creating snapshot " + snapshot + " with volume id " + volumes_dict[snapshot] + "and the error is: \n" + str(e)

# Printing the successfully created snapshots
print(successful_snapshots)


