# -*- coding: utf-8 -*-
"""DNA Center Issues API wrapper.

Copyright (c) 2019-2020 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from past.builtins import basestring

from ...restsession import RestSession
from ...utils import (
    check_type,
    dict_from_items_with_values,
    apply_path_params,
    dict_of_str,
)


class Issues(object):
    """DNA Center Issues API (version: 2.1.2).

    Wraps the DNA Center Issues
    API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory, request_validator):
        """Initialize a new Issues
        object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the DNA Center service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(Issues, self).__init__()

        self._session = session
        self._object_factory = object_factory
        self._request_validator = request_validator

    def issues(self,
               ai_driven=None,
               device_id=None,
               end_time=None,
               issue_status=None,
               mac_address=None,
               priority=None,
               site_id=None,
               start_time=None,
               headers=None,
               **request_parameters):
        """Intent API to get a list of global issues, issues for a specific
        device, or issue for a specific client device's MAC
        address.

        Args:
            start_time(int): Starting epoch time in milliseconds of
                query time window.
            end_time(int): Ending epoch time in milliseconds of
                query time window.
            site_id(basestring): Assurance UUID value of the site in
                the issue content.
            device_id(basestring): Assurance UUID value of the
                device in the issue content.
            mac_address(basestring): Client's device MAC address of
                the issue (format xx:xx:xx:xx:xx:xx).
            priority(basestring): The issue's priority value (One of
                P1, P2, P3, or P4)(Use only when
                macAddress and deviceId are not
                provided).
            ai_driven(basestring): The issue's AI driven value (Yes
                or No)(Use only when macAddress and
                deviceId are not provided).
            issue_status(basestring): The issue's status value (One
                of ACTIVE, IGNORED, RESOLVED) (Use only
                when macAddress and deviceId are not
                provided).
            headers(dict): Dictionary of HTTP Headers to send with the Request
                .
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            MyDict: JSON response. Access the object's properties by using
            the dot notation or the bracket notation.

        Raises:
            TypeError: If the parameter types are incorrect.
            MalformedRequest: If the request body created is invalid.
            ApiError: If the DNA Center cloud returns an error.
        """
        check_type(headers, dict)
        check_type(start_time, int)
        check_type(end_time, int)
        check_type(site_id, basestring)
        check_type(device_id, basestring)
        check_type(mac_address, basestring)
        check_type(priority, basestring)
        check_type(ai_driven, basestring)
        check_type(issue_status, basestring)
        if headers is not None:
            if 'X-Auth-Token' in headers:
                check_type(headers.get('X-Auth-Token'),
                           basestring, may_be_none=False)

        params = {
            'startTime':
                start_time,
            'endTime':
                end_time,
            'siteId':
                site_id,
            'deviceId':
                device_id,
            'macAddress':
                mac_address,
            'priority':
                priority,
            'aiDriven':
                ai_driven,
            'issueStatus':
                issue_status,
        }
        params.update(request_parameters)
        params = dict_from_items_with_values(params)

        path_params = {
        }

        with_custom_headers = False
        _headers = self._session.headers or {}
        if headers:
            _headers.update(dict_of_str(headers))
            with_custom_headers = True

        e_url = ('/dna/intent/api/v1/issues')
        endpoint_full_url = apply_path_params(e_url, path_params)
        if with_custom_headers:
            json_data = self._session.get(endpoint_full_url, params=params,
                                          headers=_headers)
        else:
            json_data = self._session.get(endpoint_full_url, params=params)

        return self._object_factory('bpm_5e863b7b4a4bb2f9_v2_1_2', json_data)

    def get_issue_enrichment_details(self,
                                     headers=None,
                                     **request_parameters):
        """Enriches a given network issue context (an issue id or end
        user’s Mac Address) with details about the issue(s),
        impacted hosts and suggested actions for remediation.

        Args:
            headers(dict): Dictionary of HTTP Headers to send with the Request
                .
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            MyDict: JSON response. Access the object's properties by using
            the dot notation or the bracket notation.

        Raises:
            TypeError: If the parameter types are incorrect.
            MalformedRequest: If the request body created is invalid.
            ApiError: If the DNA Center cloud returns an error.
        """
        check_type(headers, dict)
        if headers is not None:
            if 'entity_type' in headers:
                check_type(headers.get('entity_type'),
                           basestring, may_be_none=False)
            if 'entity_value' in headers:
                check_type(headers.get('entity_value'),
                           basestring, may_be_none=False)
            if 'X-Auth-Token' in headers:
                check_type(headers.get('X-Auth-Token'),
                           basestring, may_be_none=False)

        params = {
        }
        params.update(request_parameters)
        params = dict_from_items_with_values(params)

        path_params = {
        }

        with_custom_headers = False
        _headers = self._session.headers or {}
        if headers:
            _headers.update(dict_of_str(headers))
            with_custom_headers = True

        e_url = ('/dna/intent/api/v1/issue-enrichment-details')
        endpoint_full_url = apply_path_params(e_url, path_params)
        if with_custom_headers:
            json_data = self._session.get(endpoint_full_url, params=params,
                                          headers=_headers)
        else:
            json_data = self._session.get(endpoint_full_url, params=params)

        return self._object_factory('bpm_868439bb4e89a6e4_v2_1_2', json_data)
