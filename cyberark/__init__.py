#!/usr/bin/env python

import requests
import json

class CyberArk:
  def __init__(self, baseurl, username, password):
   url = baseurl+"/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logon"
   headers = {"Content-Type": "application/json"}
   data = "{\
     \"username\": \""+username+"\",\
     \"password\": \""+password+"\",\
     \"useRadiusAuthentication\": \"false\",\
     \"connectionNumber\": \"1\"\
   }"
   response = requests.request("POST", url, data=data, headers=headers)
   self.baseurl = baseurl
   self._token = reduce(lambda x, y: x[y], ["CyberArkLogonResult"], json.loads(response.text))
   self._headers = {
     "Authorization": self._token,
     "Content-Type": "application/json"
   }

  def logoff(self):
    url = self.baseurl+"/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logoff"
    response = requests.request("POST", url, headers=self._headers)
    return response.text

  def list_safes(self):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Safes"
    response = requests.request("GET", url, headers=self._headers)
    return response.text

  def get_safe_details(self, safe):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Safes/"+safe
    response = requests.request("GET", url, headers=self._headers)
    return response.text

  def get_account_details(self, safe, criteria):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Accounts"
    query = {
      "Keywords": criteria,
      "Safe": safe
    }
    response = requests.request("GET", url, headers=self._headers, params=query)
    return response.text

  def delete_account(self, account_id):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Accounts/"+account_id
    response = requests.request("DELETE", url, headers=self._headers)
    return response.text

  def add_account(self, safe, platform_id, address, account_name, username, password, disable_auto_mgmt, disable_auto_mgmt_reason, group_name, group_platform_id, properties):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Account"
    data = "{\
      \"account\": {\
        \"safe\": \""+safe+"\",\
        \"platformID\": \""+platform_id+"\",\
        \"address\": \""+address+"\",\
        \"accountName\": \""+account_name+"\",\
        \"username\": \""+username+"\",\
        \"password\": \""+password+"\",\
        \"disableAutoMgmt\": \""+disable_auto_mgmt+"\",\
        \"disableAutoMgmtReason\": \""+disable_auto_mgmt_reason+"\",\
        \"groupName\": \""+group_name+"\",\
        \"groupPlatformID\": \""+group_platform_id+"\",\
        \"properties\":\
          [\
    "
    for k, v in properties.items():
      data += "{\"Key\": \""+k+"\", \"Value\": \""+v+"\"},\
      "
    data += "]\
      }\
    }"
    response = requests.request("POST", url, data=data, headers=self._headers)
    return response.text
