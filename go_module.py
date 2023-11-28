import godaddypy

account = godaddypy.Account(api_key='fYAyEtWGwDbG_2jRRQZCugT9DP8Y4RXj21K', api_secret='4M8yHC5FH2j9GJAycJCT8X')
client = godaddypy.Client(account)


def record_exists(domain, record_type, record_name):
  records = client.get_records(domain, record_type=record_type)
  for record in records:
    if record['name'] == record_name:
      return True
  return False

def update_or_add_record(domain, record_type, record_name, record_data):
  if record_exists(domain, record_type, record_name):
    record = {'data': record_data, 'name': record_name, 'type': record_type} 
    client.update_record(domain, record)
    print(f'Updated {record_type} record for {record_name}.{domain} with data => {record_data}')

  else:
    client.add_record(domain, {'data': record_data, 'name': record_name, 'type': record_type})
    print(f'Added {record_type} record for {record_name}.{domain} with data => {record_data}')


def add_record(domain, record_type, record_name, record_data):
    client.add_record(domain, {'data': record_data, 'name': record_name, 'type': record_type})
    print(f'Added {record_type} record for {record_name}.{domain} with data => {record_data}')
