TESTLINK_API_PYTHON_DEVKEY="97e3c64c761468d6360e0a0f901be1e0"
TESTLINK_API_PYTHON_SERVER_URL="http://testtools.int.ves.solutions:8085/testlink/lib/api/xmlrpc/v1/xmlrpc.php"

import testlink

tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
tls.bulkTestCaseUpload('fred.knight', '/home/fred.knight/test-automation/monkey_scripts/mc_android/test_android_build_info.py')