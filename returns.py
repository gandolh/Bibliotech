from checking_transactions import evaluate_get_transaction
from auth_tokens_generators import encode_auth_token as enc_at,\
    decode_auth_token as dec_at
from formating_text import formatare_csv
import datetime


def add_penalty_points(auth_token, tr_id):
    data = ''
    tr_id = str(tr_id)
    with open('databases/accounts_db.csv', 'r') as fl:
        line = fl.readline()
        while line:
            lazy_list = line.split(';')
            if lazy_list[2] == dec_at(auth_token):
                lazy_list[5] = str(int(lazy_list[5])+1)
            data += ";".join(lazy_list)
            line = fl.readline()
    with open('databases/accounts_db.csv', 'w') as fl:
        fl.write(data)
    with open('databases/penalty_logs.csv', 'a') as fl:
        fl.write(formatare_csv({
            'email': dec_at(auth_token),
            'start_data': datetime.datetime.utcnow(),
            'period': 30
        }))
    # modifica si statusul la carte


def evaluate_return(auth_token, tr_id):
    remaining_time = evaluate_get_transaction(
        auth_token, tr_id).get('remaining_time')
    if remaining_time == None:
        return{
            'errorMessage': 'this transaction does not exist. Check again the id'
        }
    if int(remaining_time.split(' ')[0]) < 0:
        return{
            'Succes': 'The return request had been processed but you\'ve got one penalty point'
        }
    return{
    'Succes': 'The return request had been processed good!'
    }

def reduce_expired_penalties():
    with open('databases/accounts_db.csv', 'r') as fl:
        number_of_penalties = 0
        users_data = ''
        pen_log_data = ''
        users_line = fl.readline()
        while users_line:
            user_data_list = users_line.split(';')
            email = user_data_list[2]
            penalty_points = user_data_list[5]
            if int(penalty_points) > 0:
                with open('databases/penalty_logs.csv', 'r') as pen_log:
                    pen_log_line = pen_log.readline()
                    number_of_penalties = 0
                    while pen_log_line:
                        log_list = pen_log_line.split(';')
                        remaining_time=str(datetime.datetime.strptime \
                    		(log_list[1], '%Y-%m-%d %H:%M:%S.%f') + \
							datetime.timedelta(days=int(log_list[2])) - \
							datetime.datetime.utcnow())
                        if log_list[0] == email and int(remaining_time.split(' ')[0])<0:
                            number_of_penalties += 1
                            pen_log_line = ''
                        pen_log_data += pen_log_line
                        pen_log_line = pen_log.readline()
                    # print(number_of_penalties)
            user_data_list[5] =str(int(user_data_list[5])-int(number_of_penalties))
            users_data+=';'.join(user_data_list)
            users_line = fl.readline()
        with open('databases/accounts_db.csv','w') as fl:
        	fl.write(users_data)
        with open('databases/penalty_logs.csv','w') as fl:
        	fl.write(pen_log_data)
            #updateaza tabelele de user_data si users line

def get_request_id():
    with open('databases/return_request_db.csv','r') as fl:
        line=fl.readline();
        id=line.split(';')[0];
        while line:
            id=line.split(';')[0];
            line=fl.readline();
        # return id
        if id != '':
            return str(int(id)+1)
        else: return 0
def add_to_request_db(auth_token,tr_id):
    with open('databases/return_request_db.csv','a+') as fl:
        fl.write(formatare_csv({
            'id':get_request_id(),
            'transaction_id': str(tr_id),
            'solved':0
            }))
def get_user_type(auth_token):
    email=dec_at(auth_token)
    with open('databases/accounts_db.csv','r') as fl:
        line=fl.readline();
        while line:
            lazy_list=line.split(';');
            # print(lazy_list)
            if lazy_list[2]==email:
                return lazy_list[4]
            line=fl.readline();


def evaluate_returns(auth_token):
    usr_type=get_user_type(auth_token)
    if usr_type==0:
        return{
        'errorMessage': 'you have no permission to get here'
        }
    list_of_requests=[];
    with open('databases/return_request_db.csv') as fl:
        line=fl.readline()
        while line:
            lazy_list=line.split(';')
            list_of_requests.append({
                'id':lazy_list[0],
                'transaction_id': lazy_list[1],
                'solved':0
                })
            line=fl.readline()
        # print(list_of_requests)
        if list_of_requests:
            return {
            'return_requests':list_of_requests}
        else: return{
        'errorMessage':'No request found boss'
        }
def find_req_by_id(return_id):
    with open('databases/return_request_db.csv','r') as fl:
        line=fl.readline()
        while line:
            if str(return_id) == str(line.split(';')[0]) and \
            str(line.split(';')[2])=='0':
                return True
            line=fl.readline()
        return False
def godly_aprove(auth_token,return_id):
        if not find_req_by_id(return_id):
            return {
            'errorMessage':'this return request doesnt exist or it had been solved'
            }
        return {'Succes':'You godly aproved the request'}
def update_request_db(return_id):
    data=''
    with open('databases/return_request_db.csv','r') as fl:
        line=fl.readline()
        while line:
            lazy_list=line.split(';')
            if str(lazy_list[0])==str(return_id):
                lazy_list[2]='1';
            data+=';'.join(lazy_list);
            line=fl.readline()
    with open('databases/return_request_db.csv','w') as fl:
        fl.write(data)

def get_transaction_id_by_return_id(return_id):
    with open('databases/return_request_db.csv','r') as fl:
        line=fl.readline()
        while line:
            lazy_list=line.split(';')
            if str(lazy_list[0])==str(return_id):
                return lazy_list[1]
            line=fl.readline()   
def update_transactions_db(return_id):
    tr_id=get_transaction_id_by_return_id(return_id)
    data=''
    with open('databases/transactions_db.csv','r') as fl:
        line=fl.readline()
        while line:
            if str(line.split(';')[0])==str(tr_id):
                line=line.replace('in desfasurare','incheiat')
            data+=line;
            line=fl.readline()
    with open('databases/transactions_db.csv','w') as fl:
        fl.write(data)



if __name__ == '__main__':
    auth_tok='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM4MzM4MDksImlhdCI6MTYxMzc0NzQwOSwic3ViIjoiaW5jYW1lcmdlQGluY2FwdXRpbi5jb20ifQ.uP_DjrA1OyPnMfb9eoVfxtZpwR8nqIWTlDegW14cSW8'
    # add_to_request_db(auth_tok,'3')
    # reduce_expired_penalties()
    # print(evaluate_returns(auth_tok))
    # print(evaluate_returns(auth_tok))
    # print(godly_aprove(auth_tok,'1'))
    # update_request_db('1')
    # update_transactions_db('1')
    pass
