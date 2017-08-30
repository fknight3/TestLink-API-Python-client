import os
import sys
import testlink
# Path to Test File
sys.path.append(os.path.abspath(""))
# Path to Test supporting libs
sys.path.appsend(os.path.abspath(""))
from test_android_status_bar import TestAndroidStatusBar

TESTLINK_API_PYTHON_DEVKEY= ""
TESTLINK_API_PYTHON_SERVER_URL= ""

tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
#tls.bulkTestCaseUpload(username, test file full path, testlinkparams)
tls.bulkTestCaseUpload('fred.knight', '/home/fred.knight/test-automation/android_view_client/mc_android/test_android_pam_ldap.py', TestAndroidStatusBar.testlink_params)