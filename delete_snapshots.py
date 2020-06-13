import boto3

# Creating client for EC2 service and passing the the AWS Access Key ID and AWS Secret Access Key as parameters
client = boto3.client('ec2', region_name='us-east-1', aws_access_key_id='', aws_secret_access_key='')

# Creating a dictionary with names of instances as the key and their volume ids as the value
volumes_dict = {
    'database-1' : 'vol-0bd246509bb1ad386',
    'database-2' : 'vol-0749649f64590da2e'
}
# create a list of snapshot-ids which were deleted successfully
deleted_snapshots = []
# working for each volumeid
for snapshot in volumes_dict:
    snapshots_list = client.describe_snapshots(Filters=[
        {
            'Name': 'volume-id',
            'Values': [
                '{}'.format(volumes_dict[snapshot]),
            ]
        }
    ])
    print(snapshots_list)
    # snapshots_list is the response dictionary of client.describe_snapshots() method which contains 
    # 'Snapshots' and 'ResponseMetadata'. snapshots_list['Snapshots'] is list of snapshot ids of given volume-id
    # roughly the structure of snapshots_list would be {'Snapshots': ['snap1','snap2'], 'ResponseMetadata': {'RequestId': '757f9e'...}}
    if snapshots_list['ResponseMetadata']['HTTPStatusCode'] == 200:
        # iterate through the list of snapshot ids of snapshots_list['Snapshots'] and perform deletion of each
        for snapshot in snapshots_list['Snapshots']:
            snapshot_id = snapshot['SnapshotId']
            response = client.delete_snapshot(SnapshotId=snapshot_id, DryRun=False)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                deleted_snapshots.append(snapshot_id)
# print the snapshot-ids which were deleted successfully
print(deleted_snapshots)