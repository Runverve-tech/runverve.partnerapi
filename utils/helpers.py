import re
import requests
import json
import platform
import subprocess

def ping_server(host):
    """
    Returns True if host (str) responds to a ping request.
    """
    # Option for the number of packets
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    # Building the command
    command = ['ping', param, '1', host]
    
    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0

def make_api_request(url, method='GET', data=None, headers=None):
    """
    Helper function to make API requests
    """
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            return {'error': 'Invalid method specified'}, 400
        
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}, 500