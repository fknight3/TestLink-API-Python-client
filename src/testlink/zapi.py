import json
import cgi
import requests
import urllib2, base64

username = 'cory.gestido'
password = 'ADDPWHERE'  # input("What is your password? ")

class Zapi():

	@classmethod
	def get_ticket_title(cls, jira_number):
		jira_story_uri = "https://jira.di2e.net/rest/api/latest/issue/" + jira_number.strip()

		response = requests.get(jira_story_uri, auth=(username, password))  # send auth unconditionally
		response.raise_for_status()  # raise an exception if the authentication fails

		json_ticket_details = json.loads(response.text)
		jira_description = str(json_ticket_details['fields']['summary'])
		return jira_description

	@classmethod
	def get_ticket_type(cls, jira_number):
		jira_story_uri = "https://jira.di2e.net/rest/api/latest/issue/" + jira_number.strip()

		response = requests.get(jira_story_uri, auth=(username, password))  # send auth unconditionally
		response.raise_for_status()  # raise an exception if the authentication fails

		json_ticket_details = json.loads(response.text)
		jira_ticket_type = str(json_ticket_details['fields']['issuetype']['name'])
		return jira_ticket_type

