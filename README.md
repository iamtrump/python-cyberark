# Python CyberArk module
The module implements few CyberArk API functions.
## Requirements
* CyberArk 9.3+
## Installation
```
pip install git+https://github.com/iamtrump/python-cyberark.git
```
## Code example
```
import cyberark

ca = cyberark.CyberArk("https://cyberark.local", "my_login", "password")
# List safes:
print(ca.list_safes())
# Print account details
print(ca.get_account_details("Safe", "Account_name"))
ca.logoff()
```
