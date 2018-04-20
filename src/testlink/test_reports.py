import os
import sys
import testlink
import time
from bs4 import BeautifulSoup
from json2html import *
import json

# # Path to Test File
# sys.path.append(os.path.abspath("/home/cgestido/Test/test-automation/hybrid_os_suite/mc_xorg/gnome"))
# # Path to Test supporting libs
# sys.path.append(os.path.abspath("/home/cgestido/Test/test-automation/hybrid_os_suite/libs"))
# from test_login_ui import TcLoginUi
#
#TESTLINK_API_PYTHON_DEVKEY = "97e3c64c761468d6360e0a0f901be1e0"
#TESTLINK_API_PYTHON_SERVER_URL = "http://testtools.int.ves.solutions:8085/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
#
# tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
# tls.bulkTestCaseUpload('cgestido', '/home/cgestido/Test/test-automation/hybrid_os_suite/mc_xorg/gnome/test_login_ui.py', TcLoginUi)

#tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)


def iterTCases(api, TProjName, date1, date2):
	TProjId = api.getTestProjectByName(TProjName)['id']
	ProjList = api.getFirstLevelTestSuitesForTestProject(TProjId)
	for TSinfo in api.getFirstLevelTestSuitesForTestProject(TProjId):
		TSuiteId = TSinfo['id']
		#if details == None:
		details = 'only_id'
		for TCid in api.getTestCasesForTestSuite(TSuiteId, True, details):
			TCdata = api.getTestCase(TCid)[0]  # really only one TC?
			# customadded = api.getTestCaseCustomFieldDesignValue(TCdata['tc_external_id'],
			# 	TCdata['version'], TProjId, 'JIRA Story', 'simple')
			dateTC = time.strptime(TCdata['creation_ts'][:10], '%Y-%m-%d')
			if (date1 <= dateTC) and (dateTC <= date2):
				yield TCdata


if __name__ == '__main__':
	tlapi = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
	projName = 'Hybrid OS'
	currentTime = time.localtime()
	oldTime = time.localtime(time.time() - 3600 * 24 * 7)

	print('%s test cases created between %s and %s' % \
	      (projName, time.strftime('%Y-%m-%d', oldTime),
	       time.strftime('%Y-%m-%d', currentTime)))
	#finaloutput=''
	alldata = ''
	for TCdata in iterTCases(tlapi, projName, oldTime, currentTime):
		#finaloutput = finaloutput + ' ' + '  %(name)s\n %(summary)s\n %(steps)s' % TCdata + '\n' + '\n'


		for element in TCdata['steps']:
			element.pop('execution_type', None)
			element.pop('active', None)
			element.pop('id', None)
			#del element['execution_type']
		jsondump = json.dumps(TCdata['steps'])
		#whee = json.loads(jsondump)



		#raw_html = ''
		alldata = alldata + '<br><br>' + 'Test: ' + TCdata['name'] + '<br>' + json2html.convert(json=jsondump)

		#cleantext = BeautifulSoup(raw_html, "lxml").text
		#print cleantext



	with open('/home/cgestido/Desktop/output.html', 'w') as f:
		print >> f, alldata

	# with open('/home/cgestido/Desktop/output.txt', 'w') as f:
	# 	print >> f, '  %(name)s %(summary)s %(steps)s' % TCdata
