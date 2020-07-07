'''
auth.py
-------

Summary:

Defines a custom LDAPGroupType "GroupMembershipDNGroupType" to handle
group membership authentication tests and approval/rejection; and
implements an "assign_user_status" callback which is triggered by the
Django "populate_user" signal to correctly set is_staff and
is_superuser flags (RSEAdmin REQUIRES superuser status to function)

Background:

The UoM/ITS implementation of LDAP groups is unusual and doesn't seem
to follow any of the standard approaches as defined in the
django_auth_ldap documentation. It was therefore a challenge to test
if otherwise authenticated users are members of one (or more) groups
and set the necessary Django user flags.

Solution:

Setup django_auth_ldap settings as required for user authentication
(correct password etc) and then use the same user search query for
group search too (this must be defined though it's not used directly)

The custom GroupMembershipDNGroupType GroupType class implements new
functionality to test if the returned user data has a groupMembership
attribute that matches the one defined in the settings.

Once the user is authenticated (both username/password and group
membership requirements) the process moves onto the preparation of
the Django user data. The django_auth_ldap signal "populate_user"
triggers the assign_user_status method, which can check again (or
possibly check other defined groups) to see if is_staff and
is_superuser flags may be set to True.



x The values of settings.XAUTH_LDAP_REQUIRE_IS_STAFF_GROUP and
x settings.XAUTH_LDAP_REQUIRE_IS_SUPERUSER_GROUP entries can then be tested
x against entries in the kwargs['ldap_user'].attrs['groupMembership'] object. The
x latter is returned by the UoM/ITS LDAP Active Directory service.

x Notes:
x Both settings.XAUTH_LDAP_REQUIRE_IS_STAFF_GROUP and settings.XAUTH_LDAP_REQUIRE_IS_SUPERUSER_GROUP
x settings are additional settings provided for this solution (hence the prefix of X) and are not
x standard settings for django_auth_ldap.

'''

import ldap

from django_auth_ldap.config import LDAPSearch, LDAPGroupType
from django.conf import settings

# for settings.py
# from RSEAdmin.auth import GroupMembershipDNGroupType


class GroupMembershipDNGroupType(LDAPGroupType):
    """
    A group type that stores a list of groupMembership as distinguished names.
    """

    def __init__(self, member_attr="groupMembership", name_attr="cn"):
        """
        member_attr is the attribute on the user object that holds the list of
        member DNs.
        """
        self.member_attr = member_attr

        super().__init__(name_attr)

    def __repr__(self):
        return "<{}: {}>".format(type(self).__name__, self.member_attr)

    def user_groups(self, ldap_user, group_search):
        search = group_search.search_with_additional_terms(
            {self.member_attr: ldap_user.dn}
        )
        return search.execute(ldap_user.connection)

    def is_member(self, ldap_user, group_dn):
        try:
            result = settings.AUTH_LDAP_REQUIRE_GROUP in ldap_user.attrs[self.member_attr]
        except (ldap.UNDEFINED_TYPE, ldap.NO_SUCH_ATTRIBUTE):
            result = 0

        return result
