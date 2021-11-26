import hmac
import hashlib


async def hmac_sha256(secret_key, req):
    paramString = ""

    if "params" in req:
        for key in sorted(req['params']):
            paramString += key
            paramString += str(req['params'][key])

    sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])

    req['sig'] = hmac.new(
        bytes(str(secret_key), 'utf-8'),
        msg=bytes(sigPayload, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
