import requests


template_id = 9
survey_variables = {
    "host_list": "firsttarget",
    "filename": "/home/potest/frompython"  
}

tower_host = 'http://172.206.194.198'  # Replace with your AWX Tower host URL
username = 'admin'  # Replace with your AWX Tower username
password = 'pass'  # Replace with your AWX Tower password
user_id = 1  # Replace with the user ID

# Token creation data
token_data = {
    "description": "Tower CLI",
    "application": None,
    "scope": "write"
}

# Authenticate and create personal access token
auth_url = f'{tower_host}/api/v2/users/{user_id}/personal_tokens/'
auth_response = requests.post(auth_url, auth=(username, password), headers={'Content-Type': 'application/json'}, json=token_data, verify=False)

if auth_response.status_code == 201:
    token = auth_response.json()['token']
    headers = {'Authorization': 'Bearer ' + token}
    # Trigger the job using the template ID and survey variables
    job_template_endpoint = tower_host + f'/api/v2/job_templates/{template_id}/launch/'
    launch_data = {'extra_vars': json.dumps(survey_variables)}
    launch_response = requests.post(job_template_endpoint, headers=headers, json=launch_data, verify=False)

    if launch_response.status_code == 201:
        print(f"Job triggered successfully for template ID {template_id}")
    else:
        print(f"Failed to trigger job. Status code: {launch_response.status_code}")
        print(f"Response: {launch_response.text}")
else:
    print(f"Failed to authenticate and obtain the personal access token. Status code: {auth_response.status_code}")
    print(f"Response: {auth_response.text}")
    
