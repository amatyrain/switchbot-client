import time
import hashlib
import hmac
import base64
import uuid
import requests


class SwitchbotClient:
    def __init__(self, secret, token):
        self.base_url = "https://api.switch-bot.com"

        apiHeader = {}
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        print ('Authorization: {}'.format(token))
        print ('t: {}'.format(t))
        print ('sign: {}'.format(str(sign, 'utf-8')))
        print ('nonce: {}'.format(nonce))

        #Build api header JSON
        apiHeader['Authorization']=token
        apiHeader['Content-Type']='application/json'
        apiHeader['charset']='utf8'
        apiHeader['t']=str(t)
        apiHeader['sign']=str(sign, 'utf-8')
        apiHeader['nonce']=str(nonce)

        self.headers = apiHeader

    def _request(self, method, endpoint, data=None):
        response = requests.request(method, f'{self.base_url}{endpoint}', headers=self.headers, data=data)
        response.raise_for_status()

        return response

    def get_devices(self):
        endpoint = "/v1.1/devices"
        method = "GET"

        response = self._request(
            method=method,
            endpoint=endpoint,
        )

        return response.json()

    def get_device_status(self, device_id):
        endpoint = f"/v1.1/devices/{device_id}/status"
        method = "GET"

        response = self._request(
            method=method,
            endpoint=endpoint,
        )

        return response.json()

    def send_command(self, device_id, command, parameter=None, command_type=None):
        endpoint = f"/v1.1/devices/{device_id}/commands"
        method = "POST"
        data = {
            "command": command,
            "parameter": parameter,
            "commandType": command_type
        }

        response = self._request(
            method=method,
            endpoint=endpoint,
            data=data,
        )

        return response.json()
