import requests
import json
import constant

def generate_ticket_on_jira(row, base64Authentication):
    # Prepare payload data
    project_key = constant.project_key

    if row.title != '':
        summary = row.title
    elif row.summarized_title != '':
        summary = row.summarized_title
    else:
        summary = row.text

    description = row.text + '\n\n' + '*Version:* ' + row.version + '\n' + '*Created Date:* ' + row.created_date + '\n' + '*Link:* ' + row.url
    priority = constant.priority_id
    label = 'iOS' if row.platform == 'iOS' else 'Android'
    component_id = constant.ios_components_id if row.platform == 'iOS' else constant.android_companents_id

    if row.bug_predict == 'Bug':
        issue_type_id = constant.bug_issue_type_id
    elif row.feature_predict == 'Feature':
        issue_type_id = constant.feature_issue_type_id
    else:
        return

    payload = json.dumps({
      "fields": {
        "project": {
          "key": project_key
        },
        "summary": summary,
        "description": description,
        "issuetype": {
          "id": issue_type_id
        },
        "priority": {
          "id": priority
        },
        "labels": [
            label
        ],
        "components": [
          {
            "id": component_id
          }
        ]
      }
    })

    # Connect Jira's apis
    headers = constant.headers
    headers['Authorization'] = 'Basic ' + base64Authentication

    response = requests.request(
       "POST",
       constant.url_issue,
       data=payload,
       headers=headers
    )

    # Show result
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
