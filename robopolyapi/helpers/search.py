#!/usr/bin/env python
import ldap
import sys

class SciperSearch:
    def __init__(self):
        # demo script to search for user details
        try:
            self.l = ldap.open("ldap.epfl.ch")
            self.l.protocol_version = ldap.VERSION3
        except ldap.LDAPError, e:
            print e
        self.dn = "o=epfl,c=ch"
        self.scope = ldap.SCOPE_SUBTREE

    def get_attributes(self, sciper, attribs=None):
        '''
        Returns attributes for a given user

        Input: a dictionary of ldap attributes
        '''
        if attribs is None:
            attribs = ['givenName', 'sn', 'mail', 'displayName']
        searchFilter = "uniqueIdentifier=%s" % sciper

        ldap_result_id = self.l.search(self.dn, self.scope, searchFilter, attribs)
        result_set = []
        while 1:
            result_type, result_data = self.l.result(ldap_result_id, 0)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        res = result_set[0][0][1]
        return res

    def get_tuple(self, sciper):
        '''
        Return a tuple of attributes for use in the database

        Format : ('Sciper', 'FirstName', 'LastName', 'DisplayName', 'Email')
        '''
        attrs = ('uniqueIdentifier', 'givenName', 'sn', 'displayName', 'mail')
        return tuple(self.get_attributes(sciper, attrs)[key][0] for key in attrs)


    def get_name(self,sciper):
        dn = "o=epfl,c=ch"
        scope = ldap.SCOPE_SUBTREE

        # retrieve everything. We should refine this
        retrieveAttributes = None
        searchFilter = "uniqueIdentifier=%s" % sciper

        try:
            ldap_result_id = self.l.search(dn, scope, searchFilter, retrieveAttributes)
            result_set = []
            while 1:
                result_type, result_data = self.l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            name = result_set[0][0][1]['displayName']
        except ldap.LDAPError, e:
            print e
        except IndexError:
            return ["not found"]
        return name

if __name__ == "__main__":
    finduser = SciperSearch()
    args = sys.argv
    if len(args) < 2:
        sciper = "0"
    else:
        sciper = args[1]
    name = finduser.get_name(sciper)
    print name[0]
