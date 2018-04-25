import testlink
import time
from bs4 import BeautifulSoup
from json2html import *
import json
from testlink import TestlinkAPIGeneric
import zapi

tlapi = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
TprojName = 'Hybrid OS'
TProjId = tlapi.getTestProjectByName(TprojName)['id']
TITLE_WIDTH="200px"
DESC_WIDTH="550px"
LIGHT_BLUE="#B9D3EE"


# Create the test plan steps for the STP.
def create_stp_test_steps(test_plan_name):
	test_plan_id = tlapi.getTestPlanByName(TprojName, test_plan_name)
	test_results = tlapi.getTestCasesForTestPlan(test_plan_id[0]['id'])
	alldata = ''
	for testcase_id in test_results:
		TCdata = tlapi.getTestCase(testcase_id)[0]
		TCdata['jira_tickets'] = tlapi.getTestCaseCustomFieldDesignValue(TCdata['full_tc_external_id'], int(TCdata['version']), TProjId, 'JIRA Story', 'value')
		ticket_count = TCdata['jira_tickets'].count(',')
		TCdata['jira_ticket'] = TCdata['jira_tickets'].split(',')[ticket_count]
		TCdata['automation_type'] = tlapi.getTestCaseCustomFieldDesignValue(TCdata['full_tc_external_id'], int(TCdata['version']), TProjId, 'Automation Type', 'value')

		# Pull out the unwanted columns.
		for element in TCdata['steps']:
			element.pop('execution_type', None)
			element.pop('active', None)
			element.pop('id', None)
		# element['actions'] = 'abc'

		ticket_title = zapi.Zapi.get_ticket_title(TCdata['jira_ticket'])

		# FORMAT: #B9D3EE is baby blue, #4981CE is regular blue
		#
		# OUTER TABLE #
		outer_table = u'<br><br><table cellpadding="10" bgcolor="#4981CE"><tr><th><font color="white">'
		# JIRA SECTION #
		jira_info = TCdata['jira_ticket'] + ' - ' + ticket_title + '</font><br><br>'
		# SUMMARY # (Objective)
		test_objective = '<table cellpadding="10"><tr><th width=' + TITLE_WIDTH + ' bgcolor="' + LIGHT_BLUE + '">Test Objective: </th>' \
			'<td width=' + DESC_WIDTH + ' bgcolor="' + LIGHT_BLUE + '">' + json2html.convert(json=json.dumps(TCdata['summary']), escape=False,
		    table_attributes='border="1" cellpadding="10" bgcolor=' + LIGHT_BLUE) + '</td></tr>'
		# TYPE # (automated vs manual)
		test_level = '<tr><th width=' + TITLE_WIDTH + ' bgcolor="White"> Test Level: </th><td width=' + DESC_WIDTH + \
			' bgcolor="White">' + 'Medium</td></tr>'
		test_type = '<tr><th width=' + TITLE_WIDTH + ' bgcolor=' + LIGHT_BLUE + '> Test type or class: </th><td width=' + DESC_WIDTH + ' bgcolor=' + LIGHT_BLUE + '>' \
		    + json2html.convert(json=json.dumps(TCdata['automation_type']), escape=False,
		    table_attributes='border="1" cellpadding="10" bgcolor=' + LIGHT_BLUE) + '</td></tr>'
		prerequisites = '<tr><th width=' + TITLE_WIDTH + ' bgcolor="White"> Assumptions and Constraints: </th><td width='\
		    + DESC_WIDTH + ' bgcolor="White">' + json2html.convert(json=json.dumps(TCdata['preconditions']), escape=False,
		    table_attributes='border="1" cellpadding="10" bgcolor="White"') + '</td></tr></table>'

		# TEST STEPS # (All of the above + table of Test Steps (additional table) # bgcolor="#B9D3EE" is baby blue)
		alldata = alldata + outer_table + jira_info + test_objective + test_level + test_type + json2html.convert(
			json=json.dumps(TCdata['steps']), escape=False, table_attributes='border="1" cellpadding="10" bgcolor="White" width="800px"') + '</table>'

	with open('/home/cgestido/Desktop/stp_test_steps.html', 'w') as f:
		print >> f, alldata








# Create the test coverage for the STP.
# JIRA | Summary (Name of test) | Requirement | Type --- How to do this? via JIRA API?
def create_stp_jira_traceability(test_plan_name):
	test_plan_id = tlapi.getTestPlanByName(TprojName, test_plan_name)
	test_results = tlapi.getTestCasesForTestPlan(test_plan_id[0]['id'])
	alldata = ''
	resultguy = ''
	for testcase_id in test_results:
		TCdata = tlapi.getTestCase(testcase_id)[0]
		TCdata['jira_tickets'] = tlapi.getTestCaseCustomFieldDesignValue(TCdata['full_tc_external_id'],
			int(TCdata['version']), TProjId, 'JIRA Story', 'value')
		ticket_count = TCdata['jira_tickets'].count(',')
		TCdata['jira_ticket'] = TCdata['jira_tickets'].split(',')[ticket_count]
		ticket_title = zapi.Zapi.get_ticket_title(TCdata['jira_ticket'])
		ticket_type = zapi.Zapi.get_ticket_type(TCdata['jira_ticket'])
		resultguy = resultguy + '<tr><td width=50px>' + TCdata['jira_ticket'] + '</td><td width=250px>' + ticket_title +\
		            '</td><td width=80px>' + 'TODO: Epic' + '</td><td width=200px>' + ticket_type + '</td></tr>'

		## TODO: Epic

	outer_table = u'<br><br><table cellpadding="10" border="1" bgcolor="WHITE"><tr bgcolor="WHITE" \
	              ><td><b>JIRA Story</td><td><b>Summary</td><td><b>Requirement/Epic</td><td><b>Type</td></th>'

	alldata = outer_table + resultguy + '</table>'
	with open('/home/cgestido/Desktop/stp_traceability.html', 'w') as f:
		print >> f, alldata






# Create results chart
# JIRA | Summary | Execution Status | Notes
# TODO: Pull JIRA story and Summary from JIRA; Find relevant test and pull exec status
def create_str_report_results(test_plan_name):
	test_plan_id = tlapi.getTestPlanByName(TprojName, test_plan_name)
	test_results = tlapi.getTestCasesForTestPlan(test_plan_id[0]['id'])

	outer_table = u'<br><br><table cellpadding="10" border="1" bgcolor="WHITE"><tr bgcolor=' + LIGHT_BLUE + \
	              '><td><b>JIRA Story</td><td><b>Description</td><td><b>Execution Status</td><td><b>Notes</td></th>'

	resultguy = ''
	for test_result_key, test_result_value in test_results.items():
		# GET STATUS
		actual_result = ''
		if test_result_value[0]['exec_status'] == 'p':
			actual_result = 'Passed'
		elif test_result_value[0]['exec_status'] == 'f':
			actual_result = 'Failed'
		elif test_result_value[0]['exec_status'] == 'b':
			actual_result = 'Blocked'
		else:
			actual_result = 'Unknown'
			test_result_value[0]['tcversion_number'] = '1'

		# GET JIRA ASSOC WITH TEST
		jira_values = tlapi.getTestCaseCustomFieldDesignValue(
			test_result_value[0]['full_external_id'], int(test_result_value[0]['tcversion_number']), TProjId, 'JIRA Story', 'value')
		ticket_count = jira_values.count(',')
		jira_value = jira_values.split(',')[ticket_count]
		ticket_title = zapi.Zapi.get_ticket_title(jira_value)

		resultguy = resultguy + '<tr><td width=50px>' + jira_value + '</td><td width=250px>' + ticket_title \
			+ '</td><td width=80px>' + actual_result + '</td><td width=200px>'  + 'N/A' + '</td></tr>'

	alldata = outer_table + resultguy + '</table>'

	with open('/home/cgestido/Desktop/str_test_results.html', 'w') as f:
		print >> f, alldata


# Create test execution matrix
# Test | Date | Location | Tester | Hardware
def create_str_test_log(test_plan_name):
	test_plan_id = tlapi.getTestPlanByName(TprojName, test_plan_name)
	test_results = tlapi.getTestCasesForTestPlan(test_plan_id[0]['id'])

	outer_table = u'<br><br><table cellpadding="10" border="1" bgcolor="WHITE"><tr bgcolor=' + LIGHT_BLUE + \
	              '><td><b>JIRA Story</td><td><b>Date Performed</td><td><b>Location</td><td><b>Tester</td><td><b>Hardware Configuration</td></th>'

	resultguy = ''
	for test_result_key, test_result_value in test_results.items():

		# GET JIRA ASSOC WITH TEST
		jira_values = tlapi.getTestCaseCustomFieldDesignValue(
			test_result_value[0]['full_external_id'], int(test_result_value[0]['tcversion_number']), TProjId,
			'JIRA Story', 'value')
		ticket_count = jira_values.count(',')
		jira_value = jira_values.split(',')[ticket_count]

		resultguy = resultguy + '<tr><td width=80px>' + jira_value + '</td><td width=70px>' + 'TODO: Date' \
		            + '</td><td width=30px>VES</td><td width=200px>' + 'TODO: Tester' + '</td><td width=200px>' + 'TODO: Hardware' + '</td></tr>'

	alldata = outer_table + resultguy + '</table>'

	with open('/home/cgestido/Desktop/str_test_log.html', 'w') as f:
		print >> f, alldata







if __name__ == '__main__':
	create_stp_test_steps('COEV3_Sprint_58')
	create_str_report_results('COEV3_Sprint_58')
	create_stp_jira_traceability('COEV3_Sprint_58')
	create_str_test_log('COEV3_Sprint_58')

