# coding: utf-8

"""
    ExaVault API

    See our API reference documentation at https://www.exavault.com/developer/api-docs/  # noqa: E501

    OpenAPI spec version: 2.0
    Contact: support@exavault.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from exavault.api_client import ApiClient


class RecipientsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def resend_invitations_for_share(self, ev_api_key, ev_access_token, share_id, **kwargs):  # noqa: E501
        """Resend invitations to share recipients  # noqa: E501

        Resend invitations to one or all recipients attached to specified share. The most recent message that was sent for the share will be re-used for this email.  You can use [GET /shares/{id}](#operation/getShareById) to view the recipient list and message history for a share. Use [PATCH /shares/{id}](#operation/updateShareById) to add or remove recipients.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resend_invitations_for_share(ev_api_key, ev_access_token, share_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ev_api_key: API Key required to make the API call. (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param int share_id: ID of the share to resend invites for. (required)
        :param Body18 body:
        :return: ShareRecipientsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.resend_invitations_for_share_with_http_info(ev_api_key, ev_access_token, share_id, **kwargs)  # noqa: E501
        else:
            (data) = self.resend_invitations_for_share_with_http_info(ev_api_key, ev_access_token, share_id, **kwargs)  # noqa: E501
            return data

    def resend_invitations_for_share_with_http_info(self, ev_api_key, ev_access_token, share_id, **kwargs):  # noqa: E501
        """Resend invitations to share recipients  # noqa: E501

        Resend invitations to one or all recipients attached to specified share. The most recent message that was sent for the share will be re-used for this email.  You can use [GET /shares/{id}](#operation/getShareById) to view the recipient list and message history for a share. Use [PATCH /shares/{id}](#operation/updateShareById) to add or remove recipients.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resend_invitations_for_share_with_http_info(ev_api_key, ev_access_token, share_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ev_api_key: API Key required to make the API call. (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param int share_id: ID of the share to resend invites for. (required)
        :param Body18 body:
        :return: ShareRecipientsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ev_api_key', 'ev_access_token', 'share_id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method resend_invitations_for_share" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'ev_api_key' is set
        if ('ev_api_key' not in params or
                params['ev_api_key'] is None):
            raise ValueError("Missing the required parameter `ev_api_key` when calling `resend_invitations_for_share`")  # noqa: E501
        # verify the required parameter 'ev_access_token' is set
        if ('ev_access_token' not in params or
                params['ev_access_token'] is None):
            raise ValueError("Missing the required parameter `ev_access_token` when calling `resend_invitations_for_share`")  # noqa: E501
        # verify the required parameter 'share_id' is set
        if ('share_id' not in params or
                params['share_id'] is None):
            raise ValueError("Missing the required parameter `share_id` when calling `resend_invitations_for_share`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'share_id' in params:
            path_params['shareId'] = params['share_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'ev_api_key' in params:
            header_params['ev-api-key'] = params['ev_api_key']  # noqa: E501
        if 'ev_access_token' in params:
            header_params['ev-access-token'] = params['ev_access_token']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/recipients/shares/invites/{shareId}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShareRecipientsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
