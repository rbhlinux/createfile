import requests
import time

template_id = 9
survey_variables = {
    "host_list": "firsttarget",
    "filename": "/home/potest/fromheaven"  
}

tower_host = 'http://172.206.194.198'  # Replace with your AWX Tower host URL
username = 'admin'  # Replace with your AWX Tower username
password = 'Hackathon#2324'  # Replace with your AWX Tower password
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
#till here got token


if auth_response.status_code == 201:
    token = auth_response.json()['token']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
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
    

#block for fetching latest job for given template id;; map template id with tasks names    
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

time.sleep(120)
latestjob_url = f'{tower_host}/api/v2/job_templates/{template_id}/jobs/?order_by=-created'
latestjob_response =  requests.get(latestjob_url, headers=headers, verify=False)
latestjob = latestjob_response.json()['results']
job_id = latestjob[0]['id']
print(f"Job ID: {job_id}")
#block for job

jobid_url = f'{tower_host}/api/v2/job_events/?job_id={job_id}'
jobs_response = requests.get(jobid_url, headers=headers, verify=False)
if jobs_response.status_code == 200:
    job_events = jobs_response.json()
    print(f"Event ID: {job_events['results'][0]['id']}")
    print(f"Event Status: {job_events['results'][0]['summary_fields']['job']['status']}")
    print(f"Event Created: {job_events['results'][0]['created']}")
    print("------------")
else:
    print(f"Failed to retrieve job events. Status code: {auth_response.status_code}")
    print(f"Response: {auth_response.text}")
