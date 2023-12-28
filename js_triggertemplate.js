// JavaScript code that replicates the functionality of the Python code

const fetch = require('node-fetch');
const { setTimeout } = require('timers/promises');

const templateId = 9;
const surveyVariables = {
  "host_list": "firsttarget",
  "filename": "/home/potest/fromheaven"  
};

const towerHost = 'http://172.206.194.198';
const username = 'admin';
const password = 'Hackathon#2324';
const userId = 1;

// Token creation data
const tokenData = {
  "description": "Tower CLI",
  "application": null,
  "scope": "write"
};

// Authenticate and create personal access token
fetch(`${towerHost}/api/v2/users/${userId}/personal_tokens/`, {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${Buffer.from(`${username}:${password}`).toString('base64')}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(tokenData),
  rejectUnauthorized: false,
})
  .then(response => response.json())
  .then(data => {
    const token = data.token;
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    // Trigger the job using the template ID and survey variables
    fetch(`${towerHost}/api/v2/job_templates/${templateId}/launch/`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({ extra_vars: surveyVariables }),
      rejectUnauthorized: false,
    })
      .then(response => response.json())
      .then(data => {
        if (data.id) {
          console.log(`Job triggered successfully for template ID ${templateId}`);
          setTimeout(120000); // Wait for 120 seconds before fetching the latest job

          // Fetch latest job for the given template ID
          fetch(`${towerHost}/api/v2/job_templates/${templateId}/jobs/?order_by=-created`, {
            method: 'GET',
            headers: headers,
            rejectUnauthorized: false,
          })
            .then(response => response.json())
            .then(data => {
              const latestJobId = data.results[0].id;
              console.log(`Latest job ID for template ID ${templateId}: ${latestJobId}`);

              // Fetch job events for the latest job
              fetch(`${towerHost}/api/v2/job_events/?job_id=${latestJobId}`, {
                method: 'GET',
                headers: headers,
                rejectUnauthorized: false,
              })
                .then(response => response.json())
                .then(data => {
                  const event = data.results[0];
                  console.log(`Event ID: ${event.id}`);
                  console.log(`Event Status: ${event.summary_fields.job.status}`);
                  console.log(`Event Created: ${event.created}`);
                })
                .catch(error => console.error(`Failed to retrieve job events: ${error}`));
            })
            .catch(error => console.error(`Failed to fetch latest job: ${error}`));
        } else {
          console.error(`Failed to trigger job. Status code: ${data.status}`);
          console.error(`Response: ${JSON.stringify(data)}`);
        }
      })
      .catch(error => console.error(`Failed to trigger job: ${error}`));
  })
  .catch(error => console.error(`Failed to authenticate and obtain the personal access token: ${error}`));
