# -*- coding: utf-8 -*-

import ldap
import email_validator
import phonenumbers

ARCHIVEOS_DOMAIN='scupper.club'
ARCHIVEOS_BASEDN='dc=scupper,dc=club'

def anon_bind():
    ldap_url = 'ldap://' + ARCHIVEOS_DOMAIN
    connect = ldap.initialize(ldap_url)
    connect.simple_bind_s()
    return connect

def list_admins():
    c = anon_bind()
    r = c.search_s(ARCHIVEOS_BASEDN, ldap.SCOPE_SUBTREE, 'uid=*', ['displayName'])
    return r

def check_subscriber(candidate_sub):
    c = anon_bind()
    sub_dn = 'ou=People,' + ARCHIVEOS_BASEDN
    check = 'mail=' + candidate_sub
    r = c.search_s(sub_dn, ldap.SCOPE_SUBTREE, check)
    print(r)
