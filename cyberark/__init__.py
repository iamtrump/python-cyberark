#!/usr/binenv python

import requests
import json
import random

class CyberArk:
  def _request_error_handle(self, r):
    try:
      r.raise_for_status()
    except Exception as e:
      raise e

  def __init__(self, baseurl, username, password, connection_number=None):
    url = baseurl+"/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logon"
    headers = {"Content-Type": "application/json"}
    if connection_number is None or connection_number not in range(1,101):
      connection_number = random.randrange(1,101)
    data = {
      "username": username,
      "password": password,
      "useRadiusAuthentication": "false",
      "connectionNumber": connection_number
    }
    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    self._request_error_handle(response)
    self.baseurl = baseurl
    self._token = response.json()["CyberArkLogonResult"]
    self._headers = {
      "Authorization": self._token,
      "Content-Type": "application/json"
    }

  def logoff(self):
    url = self.baseurl+"/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logoff"
    response = requests.request("POST", url, headers=self._headers)
    self._request_error_handle(response)
    return response.json()

  def list_safes(self):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Safes"
    response = requests.request("GET", url, headers=self._headers)
    self._request_error_handle(response)
    return response.json()

  def get_safe_details(self, safe):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Safes/"+safe
    response = requests.request("GET", url, headers=self._headers)
    self._request_error_handle(response)
    return response.json()

  def get_account_details(self, safe, criteria):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Accounts"
    query = {
      "Keywords": criteria,
      "Safe": safe
    }
    response = requests.request("GET", url, headers=self._headers, params=query)
    self._request_error_handle(response)
    return response.json()

  def delete_account(self, account_id):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Accounts/"+account_id
    response = requests.request("DELETE", url, headers=self._headers)
    self._request_error_handle(response)
    return response.text

  def add_account(self, safe, platform_id, address, account_name, username, password, disable_auto_mgmt, disable_auto_mgmt_reason, group_name, group_platform_id, properties):
    url = self.baseurl+"/PasswordVault/WebServices/PIMServices.svc/Account"
    data = {
      "account": {
        "safe": safe,
        "platformID": platform_id,
        "address": address,
        "accountName": account_name,
        "username": username,
        "password": password,
        "disableAutoMgmt": str(disable_auto_mgmt).lower(),
        "disableAutoMgmtReason": disable_auto_mgmt_reason,
        "groupName": group_name,
        "groupPlatformID": group_platform_id,
        "properties": []
      }
    }
    
    for k, v in properties.items():
      prop = {"Key": k, "Value": v}
      data["account"]["properties"].append(prop)
    response = requests.request("POST", url, data=json.dumps(data), headers=self._headers)
    self._request_error_handle(response)
    return response.text
