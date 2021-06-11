project_key = 'AT'
bug_issue_type_id = '10004'
feature_issue_type_id = '10001'
priority_id = '3' # medium
ios_components_id = '10000'
android_companents_id = '10001'

endpoint = "https://pkittisak.atlassian.net/rest/api/2/"
url_issue = endpoint + "issue"
url_fields = endpoint + "field"
url_components_id = endpoint + 'project/' + project_key + '/components'

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

# https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-basic-authentication/
