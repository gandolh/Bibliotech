import jwt
#pip install pyjwt==1.4.2
import datetime


SECRET_KEY=b"\xf9'\xe4p(\xa9\x12\x1a!\x94\x8d\x1c\x99l\xc7\xb7e\xc7c\x86\x02MJ\xa0"


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            #timpul in care expira
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            #data crearii
            'iat': datetime.datetime.utcnow(),
            #user_id-ul unic
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        ).decode('ascii')
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'




if __name__ =='__main__':
    x=encode_auth_token('clopotel.admin@gmail.com')
    print(x)
    y=decode_auth_token(x)
    print(y)





