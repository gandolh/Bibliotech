from auth_tokens_generators import encode_auth_token as enc_at, decode_auth_token as dec_at
from checking_books import get_book_by_id_books
from checking_authentication import already_exist
from formating_text import formatare_csv
import datetime

def get_penalties_point(auth_token):
    with open('databases/accounts_db.csv', 'r') as fl:
        line = fl.readline()
        while line:
            lazy_list = line.split(';')
            if lazy_list[2] == dec_at(auth_token):
                return lazy_list[5]
            line = fl.readline()


def get_number_of_transactions(auth_token):
    email = dec_at(auth_token)
    no_tr = 0  # number of transactions
    last_id = 0
    with open('databases/transactions_db.csv', 'r') as fl:
        line = fl.readline()
        while line:
            print(line)
            lazy_list = line.split(';')
            last_id = lazy_list[0]
            if email in lazy_list:
                no_tr += 1
            line = fl.readline()
    # implement this,search for email in transaction db
    return no_tr, int(last_id)+1


def evaluate_transaction(auth_token, book_id, borrow_time):
    borrow_time = int(borrow_time)
    penalties_point=get_penalties_point(auth_token)
    if int(penalties_point)>=4:
        return {
        'errorMessage':'You are punished to not read!'
        }
    if borrow_time < 1:
        return {
            'errorMessage': 'your borrow time is too low'
        }
    if borrow_time > 20:
        return{
            'errorMessage': 'your borrow time is too high'
        }
    if already_exist(str(book_id), 'in desfasurare', filename='databases/transactions_db.csv') \
            or already_exist(str(book_id), 'in intarziere', filename='databases/transactions_db.csv'):
        return{
            'errorMessage': 'this book is already taken'
        }

    number_of_transactions, last_id = get_number_of_transactions(auth_token)
    if number_of_transactions >= 5:
        return{
            'errorMessage': ' you\'ve borrowed too much books.'
        }
    book_title = get_book_by_id_books(book_id).get('Title')
    return{
        'succes': 'Super, ai imprumutat {}!'.format(book_title),
        'transaction_id': last_id
    }


def evaluate_get_transaction(auth_token, transaction_id):
    with open('databases/transactions_db.csv', 'r') as fl:
        line = fl.readline()
        while line:
            lazy_list = line.split(';')
            # print(lazy_list)
            if lazy_list[0] == str(transaction_id):
                return{
                    'book_id': lazy_list[2],
                    'borrow_time': lazy_list[3],
                    'remaining_time': str(datetime.datetime.strptime(lazy_list[4], '%Y-%m-%d %H:%M:%S.%f') +
                                          datetime.timedelta(days=int(lazy_list[3])) -
                                          datetime.datetime.utcnow()),
                    # iau data de start,adun timpul de imprumut si scad data curenta
                    'number_of_extensions': lazy_list[5],
                    'status': lazy_list[6]

                }
            line = fl.readline()
    return{
        'errorMessage': 'sorry,transaction not found!'
    }


def evaluate_get_transactions(auth_token):
    # ca idee ptuem zice evaluate_get_transaction(id) si id=0 pana la
    # errorMessage dar atunci aveam complexitate 0(n^2)
    # asa ca 3bytes > n^2
    list_of_transactions = []
    email = dec_at(auth_token)
    usr_type = 0  # default = user
    # sarch for the user type in accounts_db
    with open('databases/accounts_db.csv', 'r') as fl:
        line = fl.readline()
        while line:
            lazy_list = line.split(';')
            if email in lazy_list:
                usr_type = lazy_list[4]
            line = fl.readline()
    # search for the books available for this account
    with open('databases/transactions_db.csv', 'r') as fl:
        line = fl.readline()
        while line:
            lazy_list = line.split(';')
            # print(lazy_list)
            if lazy_list[1] == email or int(usr_type) == 1:
                list_of_transactions.append({
                    'book_id': lazy_list[2],
                    'borrow_time': lazy_list[3],
                    'remaining_time': str(datetime.datetime.strptime(lazy_list[4], '%Y-%m-%d %H:%M:%S.%f') +
                                          datetime.timedelta(days=int(lazy_list[3])) -
                                          datetime.datetime.utcnow()),
                    # iau data de start,adun timpul de imprumut si scad data curenta
                    'number_of_extensions': lazy_list[5],
                    'status': lazy_list[6]

                })
            line = fl.readline()
    return list_of_transactions



def evaluate_extend_borrow(auth_token, tr_id, ext_time):
    if ext_time < 1 or ext_time > 5:
        return {
            'errorMessage': 'Pick a period between 1 and 5(inclusive)'
        }
    extended_times = evaluate_get_transaction(
        auth_token, tr_id)['number_of_extensions']
    penalties_point=get_penalties_point(auth_token)
    if int(extended_times) >= 2 or (int(extended_times)>=1 and int(penalties_point)==2 ) \
    or (int(extended_times)>=0 and int(penalties_point)==3):  # pt ca am indexarea de la 0
        return{
            'errorMessage': 'Sorry, you reached the maximum amount of extends'
        }
 
    return {
        'Succes': 'Ai extins termenul cu {} zile'.format(ext_time)
    }


def update_bt_transactions(auth_token, tr_id, extend_time):
    data = ''
    tr_id = str(tr_id)
    with open('databases/transactions_db.csv', 'r') as fl:
        line = fl.readline()
        while line:
            lazy_list = line.split(';')
            if lazy_list[0] == tr_id:
                lazy_list[3] = str(int(lazy_list[3])+extend_time)
                lazy_list[5] = str(int(lazy_list[5])+1)
            data += ";".join(lazy_list)
            line = fl.readline()
    with open('databases/transactions_db.csv', 'w') as fl:
        fl.write(data)





if __name__ == '__main__':
    auth_tok='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM4MzM4MDksImlhdCI6MTYxMzc0NzQwOSwic3ViIjoiaW5jYW1lcmdlQGluY2FwdXRpbi5jb20ifQ.uP_DjrA1OyPnMfb9eoVfxtZpwR8nqIWTlDegW14cSW8'
    # book_id = '1'
    # borrow_time = 10
    # print(evaluate_transaction(auth_tok, book_id, borrow_time))
    # evaluate_get_transaction(auth_tok,33)
    # update_bt_transactions(auth_tok, 1, 3)
    # print(evaluate_return(auth_tok,3)) # creata artificial pentru testing
    # print(evaluate_transaction(auth_tok,1,3))
    # print(evaluate_extend_borrow(auth_tok,1,3))
    pass
