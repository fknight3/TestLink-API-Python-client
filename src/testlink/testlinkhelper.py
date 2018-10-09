#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012-2017 Luiko Czub, TestLink-API-Python-client developers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# ------------------------------------------------------------------------

from builtins import object
import os
from argparse import ArgumentParser
from .version import VERSION


class TestLinkHelper(object):
    """ Helper Class to find out the TestLink connection parameters.
    a) TestLink Server URL of XML-RPC
       environment variable - TESTLINK_API_PYTHON_SERVER_URL
       default value        - http://localhost/testlink/lib/api/xmlrpc.php
       command line arg     - server_url
    b) Users devKey generated by TestLink
       environment variable - TESTLINK_API_PYTHON_DEVKEY
       default value        - 42 
       command line arg     - devKey
    c) Users devKey generated by TestLink
       environment variable - http_proxy
       default value        - not set  ('')
       command line arg     - proxy
       
    Examples 1 - init TestlinkAPIClient with environment variables 
    - define connection parameters in environment variables 
      TESTLINK_API_PYTHON_DEVKEY and TESTLINK_API_PYTHON_DEVKEY
    - TestLinkHelper().connect(TestlinkAPIClient) 
      -> returns a TestlinkAPIClient instance
      
    Examples 2 - init TestLink with command line arguments 
    - call python module with command line arguments --server_url and --devKey 
      TESTLINK_API_PYTHON_DEVKEY and TESTLINK_API_PYTHON_DEVKEY
    - tl_helper = TestLinkHelper()
      tl_helper.setParamsFromArgs()
      tl_helper.connect(TestLink) 
      -> returns a TestLink instance
    
    Attention: TL 197 changed the URL of XML-RPC 
      from  http://localhost/testlink/lib/api/xmlrpc.php
      to    http://localhost/testlink/lib/api/xmlrpc/v1/xmlrpc.php
    """

    __slots__ = ['_server_url', '_devkey', '_proxy']

    ENVNAME_SERVER_URL  = 'TESTLINK_API_PYTHON_SERVER_URL'
    ENVNAME_DEVKEY      = 'TESTLINK_API_PYTHON_DEVKEY'
    ENVNAME_PROXY       = 'http_proxy'
    DEFAULT_SERVER_URL  = 'http://localhost/testlink/lib/api/xmlrpc.php'
    DEFAULT_DEVKEY      = '42'
    DEFAULT_PROXY       = ''
    DEFAULT_DESCRIPTION = 'Python XML-RPC client for the TestLink API v%s' \
                            % VERSION

    def __init__(self, server_url=None, devkey=None, proxy=None):
        """ fill slots _server_url, _devkey and _proxy
        Priority:
        1. init args 
        2. environment variables 
        3. default values
        """
        self._server_url = server_url
        self._devkey     = devkey
        self._proxy      = proxy
        self._setParamsFromEnv()
        
    def _setParamsFromEnv(self):
        """ fill empty slots from environment variables
        _server_url <- TESTLINK_API_PYTHON_SERVER_URL
        _devkey     <- TESTLINK_API_PYTHON_DEVKEY
        _proxy      <- http_proxy
        
        If environment variables are not defined, defaults values are set.
        """
        if self._server_url is None:
            self._server_url = os.getenv(self.ENVNAME_SERVER_URL, 
                                         self.DEFAULT_SERVER_URL)
        if self._devkey is None:
            self._devkey = os.getenv(self.ENVNAME_DEVKEY, self.DEFAULT_DEVKEY)

        if not self._proxy:
            self._proxy =  os.getenv(self.ENVNAME_PROXY, self.DEFAULT_PROXY)

    def _createArgparser(self, usage):
        """ returns a parser for command line arguments """
        
        a_parser = ArgumentParser( description=usage)
        # optional command line parameters
        a_parser.add_argument('--server_url', default=self._server_url,
                help='TestLink Server URL of XML-RPC (default: %(default)s) ')
        a_parser.add_argument('--proxy', default=self._proxy,
        help='HTTP Proxy (default: %(default)s) ')
        # pseudo optional command line parameters, 
        # must be set individual for each user
        a_parser.add_argument('--devKey', default=self._devkey,
            help='Users devKey generated by TestLink (default: %(default)s) ')
        return a_parser

    def setParamsFromArgs(self, usage=DEFAULT_DESCRIPTION, args=None):
        """ fill slots from command line arguments 
        _server_url <- --server_url
        _devkey     <- --devKey
        _proxy      <- --proxy

        uses current values of these slots as default values 
        """
        a_parser = self._createArgparser(usage)
        args     = a_parser.parse_args(args)
        self._server_url = args.server_url
        self._devkey     = args.devKey
        self._proxy      = args.proxy
        
    def _getProxiedTransport(self):
        """ creates and return a ProxiedTransport with self._proxy settings """
        
        from .proxiedtransport import ProxiedTransport
        a_pt = ProxiedTransport()
        a_pt.set_proxy(self._proxy)
        return a_pt

    def connect(self, tl_api_class, **kwargs):
        """ returns a new instance of TL_API_CLASS """
        
        if self._proxy:
            kwargs['transport'] = self._getProxiedTransport()
            
        return tl_api_class(self._server_url, self._devkey, **kwargs)
