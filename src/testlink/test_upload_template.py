import os
import sys
import testlink

# Path to Test File
sys.path.append(
	os.path.abspath("/home/fred.knight/test-automation/hybrid_os_suite/mc_android/basics"))
sys.path.append(os.path.abspath("/home/fred.knight/test-automation/hybrid_os_suite/libs"))
from test_c2_attachment_processing import TcC2AttachmentProcessing

TESTLINK_API_PYTHON_DEVKEY = "97e3c64c761468d6360e0a0f901be1e0"
TESTLINK_API_PYTHON_SERVER_URL = "http://testtools.int.ves.solutions:8085/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
tls.bulkTestCaseUpload('fred.knight', '/home/fred.knight/test-automation/hybrid_os_suite/mc_android/basics/'
									  'test_c2_attachment_processing.py', TcC2AttachmentProcessing)
