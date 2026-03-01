import hcl2
import json

def scan_terraform(file_path):
    with open(file_path, 'r') as file:
        tf_config = hcl2.load(file)
        
    vulnerabilities = []
    
    if 'resource' in tf_config:
        for resource_block in tf_config['resource']:
            
            # Rule 1: S3 Buckets public access
            if 'aws_s3_bucket' in resource_block:
                for name, config in resource_block['aws_s3_bucket'].items():
                    if 'acl' in config and config['acl'] == 'public-read':
                        vulnerabilities.append({
                            'resource': name, 'type': 'aws_s3_bucket', 'severity': 'HIGH',
                            'issue': 'S3 bucket has public-read ACL.'
                        })

            # Rule 2: Security Groups with open SSH (Port 22 to 0.0.0.0/0)
            if 'aws_security_group' in resource_block:
                for name, config in resource_block['aws_security_group'].items():
                    if 'ingress' in config:
                        for ingress in config['ingress']:
                            if ingress.get('from_port') == 22 and "0.0.0.0/0" in ingress.get('cidr_blocks', []):
                                vulnerabilities.append({
                                    'resource': name, 'type': 'aws_security_group', 'severity': 'CRITICAL',
                                    'issue': 'Port 22 (SSH) is open to the public internet (0.0.0.0/0).'
                                })

            # Rule 3: Unencrypted RDS Databases
            if 'aws_db_instance' in resource_block:
                for name, config in resource_block['aws_db_instance'].items():
                    if 'storage_encrypted' in config and config['storage_encrypted'] is False:
                        vulnerabilities.append({
                            'resource': name, 'type': 'aws_db_instance', 'severity': 'HIGH',
                            'issue': 'Database storage is not encrypted at rest.'
                        })

    return vulnerabilities