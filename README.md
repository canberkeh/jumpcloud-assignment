## Requirements
This script was created using Python 3.

```
pip install -r requirements.txt
```
## Setup
For the secrets, create and fill the `.env` file. `env.sample` file is provided for reference.

## Usage
For mongodb_script.py:
    
    ```
    python mongodb_script.py
    ```

## Part 1 - MongoDB

Using mongodb_script.py will provide the following results:
- Email address of all the customers.
- Email address of customers whose favorite beer is an IPA.
- How many customers have frequented each location between 1/1/2024 - 4/1/2024.
- Favorite beers with beer name, type and the number of customers who have that beer as their favorite.
- Creates and output json file with the data above.

## Part 2
### jc_script.py
Used Jumpcloud API v1 and v2. Using the jc_script.py will provide the following results:
part-2/source.md contains the sources used for this part.
- Create and activate 2 Users.
- Create a User Group.
- Associate the 2 Users to the User Group.
- Associate one User to the recently added system.

### Tasks on Jumpcloud:
3-  
```
    echo "DEBUG" | sudo tee /opt/jc/loglevel.cache && sudo launchctl stop com.jumpcloud.darwin-agent
```
part-2/ldap-outputs/debug.log.txt.  
4- ![LDAP](https://github.com/canberkeh/jumpcloud-assignment/blob/main/part-2/assets/ldap.png)
 - ![LDAP User Groups](https://github.com/canberkeh/jumpcloud-assignment/blob/main/part-2/assets/ldap_user_groups.png)
 - ![LDAP Users in User Group](https://github.com/canberkeh/jumpcloud-assignment/blob/main/part-2/assets/users_in_user_group.png)
 - ![LDAP Users in User Group 2](https://github.com/canberkeh/jumpcloud-assignment/blob/main/part-2/assets/users_in_user_group_2.png)
 - ![LDAP Bind On](https://github.com/canberkeh/jumpcloud-assignment/blob/main/part-2/assets/ldap_bind_on.png)
  - All users bound to LDAP in your organization. 
    ```
    ldapsearch -H ldaps://ldap.jumpcloud.com:636 -x -b "ou=Users,o={ORG_ID},dc=jumpcloud,dc=com" -D "uid=TestUser33,ou=Users,o={ORG_ID},dc=jumpcloud,dc=com" -W "(objectClass=inetOrgPerson)"
    ```
    part-2/ldap-outputs/ldapsearch_output.txt

  - Just the users in one specifc user group (your choice of the two groups you created) and only returning the users email, firstname, and lastname.
    ```
    ldapsearch -H ldaps://ldap.jumpcloud.com:636 -x -b "ou=Users,o={ORG_ID},dc=jumpcloud,dc=com" -D "uid=TestUser33,ou=Users,o={ORG_ID},dc=jumpcloud,dc=com" -W "(&(objectClass=inetOrgPerson)(memberOf=cn=TestUserGroup3,ou=Users,o={ORG_ID},dc=jumpcloud,dc=com))" email givenName sn
    ```
    part-2/ldap-outputs/ldapsearch_output_filtered.txt
