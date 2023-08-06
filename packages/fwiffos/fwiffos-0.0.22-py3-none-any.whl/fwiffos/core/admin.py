# -*- coding: utf-8 -*-

import ldap

ARCHIVEOS_DOMAIN='scupper.club'
ARCHIVEOS_BASEDN='dc=scupper,dc=club'

def list_admins():
    ldap_url = 'ldap://' + ARCHIVEOS_DOMAIN
    connect = ldap.initialize(ldap_url)
    connect.simple_bind_s()
    r = connect.search_s(ARCHIVEOS_BASEDN, ldap.SCOPE_SUBTREE, 'uid=*', ['displayName'])
    return r
