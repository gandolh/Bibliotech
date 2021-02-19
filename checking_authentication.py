import re
from auth_tokens_generators import encode_auth_token as enc_at, decode_auth_token as dec_at

def checkF_name(f_name):
    return f_name.isalpha()


def checkL_name(l_name):
    return l_name.isalpha()


def already_exist(*args,filename):
	# print(args)
	with open(filename, 'r') as fl:
		line = fl.readline()
		while line:
			lazy_list = line.split(';')
			# print(lazy_list)
			for element in args:
				if element not in lazy_list:
					break;
			else: return True;
			line = fl.readline()
	return False


def check_email(email):

    rexp = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return bool(re.match(rexp, email) and not already_exist(email,filename='databases/accounts_db.csv'))


def check_password(password):
    rexp = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    return re.match(rexp, password)


def check_type(usr_type):
    return str(usr_type) in ('0', '1')


def evaluate_register(f_name, l_name, email, password, usr_type):
    if checkF_name(f_name) == False:
        return{
            'errorMessage': 'Sorry, but this first name is invalid'
        }
    elif checkL_name(l_name) == False:
        return{
            'errorMessage': 'Sorry, but this last_name is invalid'
        }
    elif check_email(email) == False:
        return{
            'errorMessage': ' Invalid or already exist Email, Sir!'
        }
    elif check_password(password) == None:
        return {
            'errorMessage': "Invalid Password, make sure you've got one letter, one number" +\
            "and one special character"
        }
    elif check_type(usr_type) == False:
        return{
            'errorMessage': 'THIS USER TYPE IS INVALID YA HACKERMAN'
        }
    else:
        return{
            'first_name': f_name,
            'last_name': l_name,
            'email': email,
            'type': usr_type  # fara a face propaganda politica la USR
        }

def evaluate_login(email,password):
	if already_exist(email,password,filename='databases/accounts_db.csv'):
		return {
		'auth_token':enc_at(email)
		}
	else: return{
		'errorMessage': 'Invalid credentials'
	}


if __name__ == '__main__':
    # print(checkName('A]a'))
    # print(checkName('A1a'))
    # print(checkName('Aa'))
    # print(check_email('clopotel@gmail.com'))
    # print(check_email('@.com'))
    # print(check_password('safepass1!'))
    # print(check_type(1))
    # print(check_email('clopotel.admingmail.com'))
    pass
