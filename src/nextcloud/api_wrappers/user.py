# -*- coding: utf-8 -*-
from nextcloud.base import WithRequester


class User(WithRequester):
    API_URL = "/ocs/v1.php/cloud/users"
    SUCCESS_CODE = 100

    def add_user(self, uid, passwd=None, displayName=None, email=None, groups=None, subadmin=None, quota=None, language=None):
        """
        Create a new user on the Nextcloud server

        :param uid: string, the required username for the new user
        :param passwd: string, the password for the new user, leave empty to send welcome mail
        :param displayName: string, the display name for the new user
        :param email: string, the email for the new user, required if password empty
        :param groups: array, the groups for the new user
        :param subadmin: array, the groups in which the new user is subadmin
        :param quota: string, quota for the new user
        :param language: string, language for the new user
        :return:
        """
        msg = {
            'userid': uid,
            'password': passwd,
            'displayName': displayName,
            'email': email,
            'groups': groups,
            'subadmin': subadmin,
            'quota': quota,
            'language': language
        }
        return self.requester.post("", msg)

    def get_users(self, search=None, limit=None, offset=None):
        """
        Retrieve a list of users from the Nextcloud server

        :param search: string, optional search string
        :param limit: int, optional limit value
        :param offset: int, optional offset value
        :return:
        """
        params = {
            'search': search,
            'limit': limit,
            'offset': offset
        }
        return self.requester.get(params=params)

    def get_user(self, uid):
        """
        Retrieve information about a single user

        :param uid: str, uid of user
        :return:
        """
        return self.requester.get("{uid}".format(uid=uid))

    def edit_user(self, uid, what, value):
        """
        Edit attributes related to a user

        Users are able to edit email, displayname and password; admins can also edit the
        quota value

        :param uid: str, uid of user
        :param what: str, the field to edit
        :param value: str, the new value for the field
        :return:
        """
        what_to_key_map = dict(
            email="email", quota="quota", phone="phone", address="address", website="website",
            twitter="twitter", displayname="displayname", password="password",
        )
        assert what in what_to_key_map, (
            "You have chosen to edit user's '{what}', but you can choose only from: {choices}"
            .format(what=what, choices=", ".join(what_to_key_map.keys()))
        )

        url = "{uid}".format(uid=uid)
        msg = dict(
            key=what_to_key_map[what],
            value=value,
        )
        return self.requester.put(url, msg)

    def disable_user(self, uid):
        """
        Disable a user on the Nextcloud server so that the user cannot login anymore

        :param uid: str, uid of user
        :return:
        """
        return self.requester.put("{uid}/disable".format(uid=uid))

    def enable_user(self, uid):
        """
        Enable a user on the Nextcloud server so that the user can login again

        :param uid: str, uid of user
        :return:
        """
        return self.requester.put("{uid}/enable".format(uid=uid))

    def delete_user(self, uid):
        """
        Delete a user from the Nextcloud server

        :param uid: str, uid of user
        :return:
        """
        return self.requester.delete("{uid}".format(uid=uid))

    def add_to_group(self, uid, gid):
        """
        Add the specified user to the specified group

        :param uid: str, uid of user
        :param gid: str, name of group
        :return:
        """
        url = "{uid}/groups".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.post(url, msg)

    def remove_from_group(self, uid, gid):
        """
        Remove the specified user from the specified group

        :param uid: str, uid of user
        :param gid: str, name of group
        :return:
        """
        url = "{uid}/groups".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.delete(url, msg)

    def create_subadmin(self, uid, gid):
        """
        Make a user the subadmin of a group

        :param uid: str, uid of user
        :param gid: str, name of group
        :return:
        """
        url = "{uid}/subadmins".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.post(url, msg)

    def remove_subadmin(self, uid, gid):
        """
        Remove the subadmin rights for the user specified from the group specified

        :param uid: str, uid of user
        :param gid: str, name of group
        :return:
        """
        url = "{uid}/subadmins".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.delete(url, msg)

    def get_subadmin_groups(self, uid):
        """
        Get the groups in which the user is a subadmin

        :param uid: str, uid of user
        :return:
        """
        url = "{uid}/subadmins".format(uid=uid)
        return self.requester.get(url)

    def resend_welcome_mail(self, uid):
        """
        Trigger the welcome email for this user again

        :param uid: str, uid of user
        :return:
        """
        url = "{uid}/welcome".format(uid=uid)
        return self.requester.post(url)
