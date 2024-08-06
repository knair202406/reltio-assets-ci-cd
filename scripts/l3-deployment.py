import sys
import requests

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_access_token(username, password, url="https://auth.reltio.com/oauth/token"):
    headers = {'Authorization': 'Basic cmVsdGlvX3VpOm1ha2l0YQ=='}
    payload = {'grant_type': 'password', 'username': username, 'password': password}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Authentication failed: {response.text}")

    return response.json().get('access_token')

def update_config(url, data, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    # Encode the data in UTF-8
    encoded_data = data.encode('utf-8')
    response = requests.put(url, data=encoded_data, headers=headers)
    return response

def main():
    if len(sys.argv) != 7:
        sys.exit(1)

    l3_path = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    reltio_environment = sys.argv[4]
    reltio_tenant_id = sys.argv[5]
    rdm_tenant_id = sys.argv[6]

    url = 'https://' + reltio_environment + '.reltio.com/reltio/api/' + reltio_tenant_id + '/configuration'

    access_token = get_access_token(username, password)
    
    l3_config = read_file(l3_path)
    l3_config = l3_config.replace('{RDM_TENANT_ID}', rdm_tenant_id)

    response = update_config(url, l3_config, access_token)

    print("Response Status Code:", response.status_code)

if __name__ == "__main__":
    main()
