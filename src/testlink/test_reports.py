import testlink
import time
from bs4 import BeautifulSoup
from json2html import *
import json

TITLE_WIDTH="200px"
DESC_WIDTH="550px"
LIGHT_BLUE="#B9D3EE"

# Go through tests and pull out the ones that meet the search criteria.
def iterTCases(api, TProjName, date1, date2):
	TProjId = api.getTestProjectByName(TProjName)['id']
	#ProjList = api.getFirstLevelTestSuitesForTestProject(TProjId)
	for TSinfo in api.getFirstLevelTestSuitesForTestProject(TProjId):
		TSuiteId = TSinfo['id']
		#if details == None:
		details = 'only_id'
		for TCid in api.getTestCasesForTestSuite(TSuiteId, True, details):
			TCdata = api.getTestCase(TCid)[0]  # really only one TC?
			TCdata['jira_tickets'] = api.getTestCaseCustomFieldDesignValue(TCdata['full_tc_external_id'], int(TCdata['version']),
				TProjId, 'JIRA Story', 'value')
			TCdata['automation_type'] = api.getTestCaseCustomFieldDesignValue(TCdata['full_tc_external_id'], int(TCdata['version']),
			    TProjId, 'Automation Type', 'value')
			dateTC = time.strptime(TCdata['creation_ts'][:10], '%Y-%m-%d')
			if (date1 <= dateTC) and (dateTC <= date2):
				yield TCdata


# Create the test plan steps for the STP.
def create_stp_test_steps():
	tlapi = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
	projName = 'Hybrid OS'
	currentTime = time.localtime()
	oldTime = time.localtime(time.time() - 3600 * 24 * 3)

	print('%s test cases created between %s and %s' % \
	      (projName, time.strftime('%Y-%m-%d', oldTime),
	       time.strftime('%Y-%m-%d', currentTime)))
	#finaloutput=''
	alldata = ''
	for TCdata in iterTCases(tlapi, projName, oldTime, currentTime):
		#finaloutput = finaloutput + ' ' + '  %(name)s\n %(summary)s\n %(steps)s' % TCdata + '\n' + '\n'

		# Pull out the unwanted columns.
		for element in TCdata['steps']:
			element.pop('execution_type', None)
			element.pop('active', None)
			element.pop('id', None)
			#element['actions'] = 'abc'

		# FORMAT: #B9D3EE is baby blue, #4981CE is regular blue
		#
		# OUTER TABLE #
		outer_table = u'<br><br><table cellpadding="10" bgcolor="#4981CE"><tr><th><font color="white">'
		# JIRA SECTION #
		jira_info = TCdata['jira_tickets'] + ' - ' + TCdata['name'] + '</font><br><br>'
		# SUMMARY # (Objective)
		test_objective = '<table cellpadding="10">' \
		    '<tr><th width=' + TITLE_WIDTH + ' bgcolor="White">Test Objective: </th><td width=' + DESC_WIDTH + ' bgcolor="White">' \
		    + json2html.convert(json=json.dumps(TCdata['summary']), escape=False,
		    table_attributes='border="1" cellpadding="10" bgcolor="White"') + '</td></tr>'
		# TYPE # (automated vs manual)
		test_level = '<tr><th width=' + TITLE_WIDTH + ' bgcolor=' + LIGHT_BLUE + '> Test Level: </th><td width=' + DESC_WIDTH + ' bgcolor=' + LIGHT_BLUE + '>' \
			+ 'Medium</td></tr>'
		test_type = '<tr><th width=' + TITLE_WIDTH + ' bgcolor="White"> Test type or class: </th><td width=' + DESC_WIDTH + ' bgcolor="White">' \
		    + json2html.convert(json=json.dumps(TCdata['automation_type']), escape=False,
			table_attributes='border="1" cellpadding="10" bgcolor="White"') + '</td></tr>'
		prerequisites = '<tr><th width=' + TITLE_WIDTH + ' bgcolor=' + LIGHT_BLUE + '> Assumptions and Constraints: </th><td width=' + DESC_WIDTH + ' bgcolor=' + LIGHT_BLUE + '>' \
		    + json2html.convert(json=json.dumps(TCdata['preconditions']), escape=False,
			table_attributes='border="1" cellpadding="10" bgcolor=' + LIGHT_BLUE + '') + '</td></tr></table>'

		# TEST STEPS # (All of the above + table of Test Steps (additional table) # bgcolor="#B9D3EE" is baby blue)
		alldata = alldata + outer_table + jira_info + test_objective + test_level + test_type + json2html.convert(json=json.dumps(TCdata['steps']),
		    escape=False, table_attributes='border="1" cellpadding="10" bgcolor="White" width="800px"') + '</table>'

	with open('/home/cgestido/Desktop/stp_test_steps.html', 'w') as f:
		print >> f, alldata

	# with open('/home/cgestido/Desktop/output.txt', 'w') as f:
	# 	print >> f, '  %(name)s %(summary)s %(steps)s' % TCdata


# Create the test coverage for the STP.
# JIRA | Summary (Name of test) | Requirement | Type --- How to do this? via JIRA API?
def create_stp_test_chart():
	print 'ohai'

# Create results chart
# JIRA | Summary | Execution Status | Notes
def create_str_report_results():
	print 'whee'

# Create test execution matrix
# Test | Date | Location | Tester | Hardware
def create_str_test_log():
	print 'ooooohyeaaahhh'




if __name__ == '__main__':
	create_stp_test_steps()

