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


class UsersApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_user(self, ev_api_key, ev_access_token, **kwargs):  # noqa: E501
        """Create a user  # noqa: E501

        Adds a new user to the account. The user may be configured as an admin or standard user, and (if a standard user) may be assigned a restricted [home directory](/docs/account/04-users/00-introduction#setting-the-user-s-home-directory) and restricted [permissions](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions).   **Notes:**  - You must be an [admin-level user](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions) to use this.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_user(ev_api_key, ev_access_token, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ev_api_key: API key required to make the API call (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param Body5 body:
        :return: UserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.add_user_with_http_info(ev_api_key, ev_access_token, **kwargs)  # noqa: E501
        else:
            (data) = self.add_user_with_http_info(ev_api_key, ev_access_token, **kwargs)  # noqa: E501
            return data

    def add_user_with_http_info(self, ev_api_key, ev_access_token, **kwargs):  # noqa: E501
        """Create a user  # noqa: E501

        Adds a new user to the account. The user may be configured as an admin or standard user, and (if a standard user) may be assigned a restricted [home directory](/docs/account/04-users/00-introduction#setting-the-user-s-home-directory) and restricted [permissions](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions).   **Notes:**  - You must be an [admin-level user](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions) to use this.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_user_with_http_info(ev_api_key, ev_access_token, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ev_api_key: API key required to make the API call (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param Body5 body:
        :return: UserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ev_api_key', 'ev_access_token', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_user" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'ev_api_key' is set
        if ('ev_api_key' not in params or
                params['ev_api_key'] is None):
            raise ValueError("Missing the required parameter `ev_api_key` when calling `add_user`")  # noqa: E501
        # verify the required parameter 'ev_access_token' is set
        if ('ev_access_token' not in params or
                params['ev_access_token'] is None):
            raise ValueError("Missing the required parameter `ev_access_token` when calling `add_user`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
            '/users', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_user(self, id, ev_api_key, ev_access_token, **kwargs):  # noqa: E501
        """Delete a user  # noqa: E501

        Delete a user from the account. Deleting a user does **NOT** delete any files from the account; it merely removes a user's access. Aternatively, locking a user via the [PATCH /users/{id}](#operation/updateUser) will keep the user in your account, but make it unable to log in.   Resources and shares owned by the deleted user will be owned by the master user after the deletion.  **Notes:**   - You must have [admin-level access](/docs/account/04-users/01-admin-users) to delete a user. - The primary owner of the account cannot be deleted.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_user(id, ev_api_key, ev_access_token, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param float id: The user's ID. Note that this is our internal ID, and _not the username_. You can obtain it by calling the [GET /users](#operation/listUsers) method. (required)
        :param str ev_api_key: API Key required to make the API call. (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :return: EmptyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_user_with_http_info(id, ev_api_key, ev_access_token, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_user_with_http_info(id, ev_api_key, ev_access_token, **kwargs)  # noqa: E501
            return data

    def delete_user_with_http_info(self, id, ev_api_key, ev_access_token, **kwargs):  # noqa: E501
        """Delete a user  # noqa: E501

        Delete a user from the account. Deleting a user does **NOT** delete any files from the account; it merely removes a user's access. Aternatively, locking a user via the [PATCH /users/{id}](#operation/updateUser) will keep the user in your account, but make it unable to log in.   Resources and shares owned by the deleted user will be owned by the master user after the deletion.  **Notes:**   - You must have [admin-level access](/docs/account/04-users/01-admin-users) to delete a user. - The primary owner of the account cannot be deleted.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_user_with_http_info(id, ev_api_key, ev_access_token, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param float id: The user's ID. Note that this is our internal ID, and _not the username_. You can obtain it by calling the [GET /users](#operation/listUsers) method. (required)
        :param str ev_api_key: API Key required to make the API call. (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :return: EmptyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'ev_api_key', 'ev_access_token']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_user" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_user`")  # noqa: E501
        # verify the required parameter 'ev_api_key' is set
        if ('ev_api_key' not in params or
                params['ev_api_key'] is None):
            raise ValueError("Missing the required parameter `ev_api_key` when calling `delete_user`")  # noqa: E501
        # verify the required parameter 'ev_access_token' is set
        if ('ev_access_token' not in params or
                params['ev_access_token'] is None):
            raise ValueError("Missing the required parameter `ev_access_token` when calling `delete_user`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'ev_api_key' in params:
            header_params['ev-api-key'] = params['ev_api_key']  # noqa: E501
        if 'ev_access_token' in params:
            header_params['ev-access-token'] = params['ev_access_token']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/users/{id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EmptyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_user_by_id(self, id, ev_api_key, ev_access_token, **kwargs):  # noqa: E501
        """Get info for a user  # noqa: E501

        Get the details for a specific user. You can use the `include` parameter to also get the details of related records, such as the account or the home directory.  **Notes:**  - You must have [admin or master](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions) access to use this.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_user_by_id(id, ev_api_key, ev_access_token, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param float id: The user's ID. Note that this is our internal ID, and _not the username_. You can obtain it by calling the [GET /users](#operation/listUsers) method. (required)
        :param str ev_api_key: API Key (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param str include: Comma-separated list of relationships to include in response. Possible values include **homeResource** and **ownerAccount**.
        :return: UserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_user_by_id_with_http_info(id, ev_api_key, ev_access_token, **kwargs)  # noqa: E501
        else:
            (data) = self.get_user_by_id_with_http_info(id, ev_api_key, ev_access_token, **kwargs)  # noqa: E501
            return data

    def get_user_by_id_with_http_info(self, id, ev_api_key, ev_access_token, **kwargs):  # noqa: E501
        """Get info for a user  # noqa: E501

        Get the details for a specific user. You can use the `include` parameter to also get the details of related records, such as the account or the home directory.  **Notes:**  - You must have [admin or master](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions) access to use this.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_user_by_id_with_http_info(id, ev_api_key, ev_access_token, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param float id: The user's ID. Note that this is our internal ID, and _not the username_. You can obtain it by calling the [GET /users](#operation/listUsers) method. (required)
        :param str ev_api_key: API Key (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param str include: Comma-separated list of relationships to include in response. Possible values include **homeResource** and **ownerAccount**.
        :return: UserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'ev_api_key', 'ev_access_token', 'include']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_user_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_user_by_id`")  # noqa: E501
        # verify the required parameter 'ev_api_key' is set
        if ('ev_api_key' not in params or
                params['ev_api_key'] is None):
            raise ValueError("Missing the required parameter `ev_api_key` when calling `get_user_by_id`")  # noqa: E501
        # verify the required parameter 'ev_access_token' is set
        if ('ev_access_token' not in params or
                params['ev_access_token'] is None):
            raise ValueError("Missing the required parameter `ev_access_token` when calling `get_user_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'include' in params:
            query_params.append(('include', params['include']))  # noqa: E501

        header_params = {}
        if 'ev_api_key' in params:
            header_params['ev-api-key'] = params['ev_api_key']  # noqa: E501
        if 'ev_access_token' in params:
            header_params['ev-access-token'] = params['ev_access_token']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/users/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_users(self, ev_api_key, ev_access_token, **kwargs):  # noqa: E501
        """Get a list of users  # noqa: E501

        Get a list of the users in your account. There are three main types of searches you can do with this method:  1. Search for a user by username. If you provide the `username` parameter in your call, then only the user who exactly matches that username will be in the list of matches. Any other parameters are ignored. 1. Search for a user by individual filter fields (`nickname`,`email`,`role`,`status`,`homeDir`). Users in the list will be ones who match all of the filters you choose to search by. For example, you could look for users with the \"admin\" `role` AND `email` addresses ending in \"*@acme.com\".  1. Search for a user by search string. If you provide the `search` parameter, users whose nickname OR email OR role OR homeDir match value your provide.  **Notes:**  - You must be an [admin-level user](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions) to use this. - The homeDir is the full path to the user's home directory, not a resource ID or hash.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_users(ev_api_key, ev_access_token, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ev_api_key: API key required to make the API call. (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param str username: The username of the user you are looking for. Only entries with the same username as this will be in the list of results. Does not support wildcard searches.
        :param str nickname: Nickname to search for. Ignored if `username` is provided. Supports wildcard searches.
        :param str email: Email to search for. Ignored if `username` is provided. Supports wildcard searches
        :param str role: Types of users to include the list. Ignored if `username` is provided. Valid options are **admin**, **master** and **user**
        :param int status: Whether a user is locked. Ignored if `username` is provided. **0** means user is locked, **1** means user is not locked. 
        :param str home_dir: Path for user's home directory. Ignored if `username` is provided. Supports wildcard searches.
        :param str search: Searches the nickname, email, role and homeDir fields for the provided value. Ignored if `username` is provided. Supports wildcard searches.
        :param int offset: Starting user record in the result set. Can be used for pagination.
        :param str sort: Sort order or matching users. You can sort by multiple columns by separating sort options with a comma; the sort will be applied in the order specified. The sort order for each sort field is ascending unless it is prefixed with a minus (“-“), in which case it will be descending.  Valid sort fields are: **nickname**, **username**, **email**, **homeDir** and **modified**
        :param int limit: Number of users to return. Can be used for pagination.
        :param str include: Comma separated list of relationships to include in response. Valid options are **homeResource** and **ownerAccount**.
        :return: UserCollectionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_users_with_http_info(ev_api_key, ev_access_token, **kwargs)  # noqa: E501
        else:
            (data) = self.list_users_with_http_info(ev_api_key, ev_access_token, **kwargs)  # noqa: E501
            return data

    def list_users_with_http_info(self, ev_api_key, ev_access_token, **kwargs):  # noqa: E501
        """Get a list of users  # noqa: E501

        Get a list of the users in your account. There are three main types of searches you can do with this method:  1. Search for a user by username. If you provide the `username` parameter in your call, then only the user who exactly matches that username will be in the list of matches. Any other parameters are ignored. 1. Search for a user by individual filter fields (`nickname`,`email`,`role`,`status`,`homeDir`). Users in the list will be ones who match all of the filters you choose to search by. For example, you could look for users with the \"admin\" `role` AND `email` addresses ending in \"*@acme.com\".  1. Search for a user by search string. If you provide the `search` parameter, users whose nickname OR email OR role OR homeDir match value your provide.  **Notes:**  - You must be an [admin-level user](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions) to use this. - The homeDir is the full path to the user's home directory, not a resource ID or hash.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_users_with_http_info(ev_api_key, ev_access_token, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ev_api_key: API key required to make the API call. (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param str username: The username of the user you are looking for. Only entries with the same username as this will be in the list of results. Does not support wildcard searches.
        :param str nickname: Nickname to search for. Ignored if `username` is provided. Supports wildcard searches.
        :param str email: Email to search for. Ignored if `username` is provided. Supports wildcard searches
        :param str role: Types of users to include the list. Ignored if `username` is provided. Valid options are **admin**, **master** and **user**
        :param int status: Whether a user is locked. Ignored if `username` is provided. **0** means user is locked, **1** means user is not locked. 
        :param str home_dir: Path for user's home directory. Ignored if `username` is provided. Supports wildcard searches.
        :param str search: Searches the nickname, email, role and homeDir fields for the provided value. Ignored if `username` is provided. Supports wildcard searches.
        :param int offset: Starting user record in the result set. Can be used for pagination.
        :param str sort: Sort order or matching users. You can sort by multiple columns by separating sort options with a comma; the sort will be applied in the order specified. The sort order for each sort field is ascending unless it is prefixed with a minus (“-“), in which case it will be descending.  Valid sort fields are: **nickname**, **username**, **email**, **homeDir** and **modified**
        :param int limit: Number of users to return. Can be used for pagination.
        :param str include: Comma separated list of relationships to include in response. Valid options are **homeResource** and **ownerAccount**.
        :return: UserCollectionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ev_api_key', 'ev_access_token', 'username', 'nickname', 'email', 'role', 'status', 'home_dir', 'search', 'offset', 'sort', 'limit', 'include']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_users" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'ev_api_key' is set
        if ('ev_api_key' not in params or
                params['ev_api_key'] is None):
            raise ValueError("Missing the required parameter `ev_api_key` when calling `list_users`")  # noqa: E501
        # verify the required parameter 'ev_access_token' is set
        if ('ev_access_token' not in params or
                params['ev_access_token'] is None):
            raise ValueError("Missing the required parameter `ev_access_token` when calling `list_users`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'username' in params:
            query_params.append(('username', params['username']))  # noqa: E501
        if 'nickname' in params:
            query_params.append(('nickname', params['nickname']))  # noqa: E501
        if 'email' in params:
            query_params.append(('email', params['email']))  # noqa: E501
        if 'role' in params:
            query_params.append(('role', params['role']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'home_dir' in params:
            query_params.append(('homeDir', params['home_dir']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'include' in params:
            query_params.append(('include', params['include']))  # noqa: E501

        header_params = {}
        if 'ev_api_key' in params:
            header_params['ev-api-key'] = params['ev_api_key']  # noqa: E501
        if 'ev_access_token' in params:
            header_params['ev-access-token'] = params['ev_access_token']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/users', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserCollectionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_user(self, ev_api_key, ev_access_token, id, **kwargs):  # noqa: E501
        """Update a user  # noqa: E501

        Updates the settings for the user. Note that the unique key for this API call is our internal ID, and _not_ the username, as the username can be changed.  In the request body, you should only send the parameters for values that you wish to change for the user.  **Notes:**  - You must have [admin or master](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions) access to edit other users. If you have user-level access, you can only update your own user settings. - You cannot edit a master user with this method.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_user(ev_api_key, ev_access_token, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ev_api_key: API key required to make the API call. (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param float id: The user's ID. Note that this is our internal ID, and _not the username_. You can obtain it by calling the [GET /users](#operation/listUsers) method. (required)
        :param Body6 body:
        :return: UserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_user_with_http_info(ev_api_key, ev_access_token, id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_user_with_http_info(ev_api_key, ev_access_token, id, **kwargs)  # noqa: E501
            return data

    def update_user_with_http_info(self, ev_api_key, ev_access_token, id, **kwargs):  # noqa: E501
        """Update a user  # noqa: E501

        Updates the settings for the user. Note that the unique key for this API call is our internal ID, and _not_ the username, as the username can be changed.  In the request body, you should only send the parameters for values that you wish to change for the user.  **Notes:**  - You must have [admin or master](/docs/account/04-users/00-introduction#managing-user-roles-and-permissions) access to edit other users. If you have user-level access, you can only update your own user settings. - You cannot edit a master user with this method.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_user_with_http_info(ev_api_key, ev_access_token, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ev_api_key: API key required to make the API call. (required)
        :param str ev_access_token: Access token required to make the API call. (required)
        :param float id: The user's ID. Note that this is our internal ID, and _not the username_. You can obtain it by calling the [GET /users](#operation/listUsers) method. (required)
        :param Body6 body:
        :return: UserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ev_api_key', 'ev_access_token', 'id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_user" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'ev_api_key' is set
        if ('ev_api_key' not in params or
                params['ev_api_key'] is None):
            raise ValueError("Missing the required parameter `ev_api_key` when calling `update_user`")  # noqa: E501
        # verify the required parameter 'ev_access_token' is set
        if ('ev_access_token' not in params or
                params['ev_access_token'] is None):
            raise ValueError("Missing the required parameter `ev_access_token` when calling `update_user`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_user`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

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
            '/users/{id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
