## API PART
https://docs.jumpcloud.com/api/1.0

https://docs.jumpcloud.com/api/2.0

Create System User
https://docs.jumpcloud.com/api/1.0/#tag/Systemusers/operation/systemusers_post

Activate User
https://docs.jumpcloud.com/api/1.0/#tag/Systemusers/operation/systemusers_state_activate

Create New User Group
https://docs.jumpcloud.com/api/2.0/index.html#tag/User-Groups/operation/groups_user_post

Associate User to Group
https://docs.jumpcloud.com/api/2.0/index.html#tag/Graph/operation/graph_userGroupMembersList

Get Members by Group ID
https://docs.jumpcloud.com/api/2.0/index.html#tag/Graph/operation/graph_userGroupMembership

Associate User to System
https://docs.jumpcloud.com/api/2.0/index.html#tag/Systems/operation/graph_systemAssociationsPost

Get All Systems
https://docs.jumpcloud.com/api/1.0/#tag/Systems/operation/systems_list

Get System Associations
https://docs.jumpcloud.com/api/2.0/index.html#tag/Systems/operation/graph_systemAssociationsList

## LDAP and Agent Logs
### LOGS
Set level to DEBUG
https://jumpcloud.com/support/set-the-log-level-to-debug?_highlight=debug#linux
```
  echo "DEBUG" | sudo tee /opt/jc/loglevel.cache && sudo launchctl stop com.jumpcloud.darwin-agent
```

Get logs using dashboard
https://jumpcloud.com/support/view-agent-logs-using-commands?_highlight=agent&_highlight=logs

### LDAP
#### LDAP Search
https://jumpcloud.com/support/use-ldapsearch-with-jumpcloud?_highlight=ldapsearch
OrgID = Settings > Organization Profile > Organization ID
```
  ldapsearch -H ldaps://ldap.jumpcloud.com:636 -x -b "ou=Users,o=66983c51208c8fcdf4288780,dc=jumpcloud,dc=com" -D "uid=TestUser33,ou=Users,o=66983c51208c8fcdf4288780,dc=jumpcloud,dc=com" -W "(objectClass=inetOrgPerson)"
```

https://jumpcloud.com/support/search-by-user-or-group-in-ldap
- I used AI to get filtered results because I couldn't find them in the JumpCloud LDAP and open source LDAP documentation.
mail, givenName, sn detected in all ldapsearch result
mail: testuser22@gmail.com
givenName: Test22
sn: User22
```
  ldapsearch -H ldaps://ldap.jumpcloud.com:636 -x -b "ou=Users,o=66983c51208c8fcdf4288780,dc=jumpcloud,dc=com" -D "uid=TestUser33,ou=Users,o=66983c51208c8fcdf4288780,dc=jumpcloud,dc=com" -W "(&(objectClass=inetOrgPerson)(memberOf=cn=TestUserGroup3,ou=Users,o=66983c51208c8fcdf4288780,dc=jumpcloud,dc=com))" email givenName sn
```