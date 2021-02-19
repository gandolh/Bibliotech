from flask import Flask, request
import datetime
from checking_authentication import evaluate_register, evaluate_login
from formating_text import formatare_csv
from auth_tokens_generators import encode_auth_token as enc_at, decode_auth_token as dec_at
from checking_books import evaluate_add_book, evaluate_get_book, evaluate_get_books
from checking_transactions import evaluate_transaction, evaluate_get_transaction,\
    evaluate_get_transactions, evaluate_extend_borrow, update_bt_transactions
from returns import evaluate_return,reduce_expired_penalties,add_penalty_points, \
add_to_request_db,evaluate_returns,godly_aprove, update_request_db, \
update_transactions_db
from review_methods import evaluate_review,add_review_to_db
app = Flask(__name__)
auth_token = 'Invalid'


@app.route('/')
def hello():
    return 'home_page'


@app.route('/register', methods=['POST'])
def register():
    register_data = request.get_json()
    # first_name = request.args.get('first_name')
    first_name = register_data['first_name']
    last_name = register_data['last_name']
    email = register_data['email']
    password = register_data['password']
    usr_type = register_data['type']
    register_data['penalties']=0;
    new_account = evaluate_register(
        first_name, last_name, email, password, usr_type)

    if 'errorMessage' not in new_account:
        with open('databases/accounts_db.csv', 'a+') as fl:
            fl.write(formatare_csv(register_data))
            # print(formatare_csv(new_account))

    return new_account


@app.route('/login', methods=['POST'])
def login():

    login_data = request.get_json()
    email = login_data['email']
    password = login_data['password']
    login_message = evaluate_login(email, password)
    # check every login if some of the 
    #penalties expired
    reduce_expired_penalties(); 
    if 'auth_token' in login_message:
        auth_token = login_message['auth_token']
    else:
        auth_token = login_message['errorMessage']
    return str(login_message)


@app.route('/book', methods=['POST'])
def add_book():
    # doar pentru Admini (usr_type==1)
    book_data = request.get_json()
    auth_token = book_data['auth_token']
    book_name = book_data['book_name']
    book_author = book_data['book_author']
    description = book_data['description']
    new_book = evaluate_add_book(
        auth_token, book_name, book_author, description)
    if 'errorMessage' not in new_book:
        with open('databases/books_db.csv', 'a+') as fl:
            fl.write(formatare_csv(new_book))
    return new_book
    # adauga o baza de date pentru recenzii


@app.route('/book', methods=['GET'])
def get_book():
    auth_token = request.args.get('auth_token')
    b_id = request.args.get('id')
    if auth_token==None:
    	searched_book = evaluate_get_book( b_id)
    else:
    	searched_book = evaluate_get_book(b_id,auth_token)
    
    return searched_book  # de adaugat recenziile aici


@app.route('/books', methods=['GET'])
def get_books():
    searched_books = evaluate_get_books()
    return searched_books


@app.route('/transaction', methods=['POST'])
def add_transaction():
    transaction_data = request.get_json()
    auth_token = transaction_data['auth_token']
    book_id = transaction_data['book_id']
    borrow_time = transaction_data['borrow_time']
    new_transaction = evaluate_transaction(auth_token, book_id, borrow_time)

    to_write_db = {
        'id': new_transaction.get('transaction_id'),
        'email': dec_at(auth_token),
        'book_id': book_id,
        'borrow_time': borrow_time,
        'start_date': datetime.datetime.utcnow(),
        # 'end_date':datetime.datetime.utcnow() + datetime.timedelta(days=borrow_time)
        'number_of_extensions': 0,
        'status': 'in desfasurare'
    }
    if 'errorMessage' not in new_transaction:
        with open('databases/transactions_db.csv', 'a+') as fl:
            fl.write(formatare_csv(to_write_db))
    return new_transaction


@app.route('/transaction', methods=['GET'])
def get_transaction():
    auth_token = request.args.get('auth_token')
    transaction_id = request.args.get('transaction_id')
    transaction_details = evaluate_get_transaction(auth_token, transaction_id)
    return transaction_details


@app.route('/transactions', methods=['GET'])
def get_transactions():
    auth_token = request.args.get('auth_token')
    transactions_details = evaluate_get_transactions(auth_token)
    return {
        'transactions': transactions_details
    }


@app.route('/extend', methods=['POST'])
def extend_borrowing():
    extend_data = request.get_json()
    auth_token = extend_data['auth_token']
    tr_id = extend_data['transaction_id']  # transaction_id
    ext_time = extend_data['extend_time']  # extend_time
    extend_bt = evaluate_extend_borrow(auth_token, tr_id, ext_time)
    if 'Succes' in extend_bt:
        update_bt_transactions(auth_token, tr_id, ext_time)
    return extend_bt


@app.route('/return', methods=['POST'])
def returning_book():
	return_data=request.get_json()
	auth_token=return_data['auth_token']
	tr_id =return_data['transaction_id']
	return_state=evaluate_return(auth_token,tr_id)
	if 'good!' not in return_state['Succes']:
		add_penalty_points(auth_token, tr_id)
	return return_state
	add_to_request_db(auth_token,tr_id);

@app.route('/returns',methods=['GET'])
def get_returns():
	auth_token = request.args.get('auth_token')
	return evaluate_returns(auth_token)

@app.route('/return/end', methods=['POST'])
def the_godly_aprove(): #accept the return of a book
	return_req_data=request.get_json()
	auth_token=return_req_data['auth_token']
	return_id=return_req_data['return_id']
	aprove_state=godly_aprove(auth_token,return_id)
	if 'Succes' in aprove_state:
		update_request_db(return_id)
		update_transactions_db(return_id)
	return aprove_state

@app.route('/review',methods=['POST'])
def post_review():
	review_data=request.get_json()
	auth_token= review_data['auth_token']
	book_id = review_data['book_id']
	rating= review_data['rating']
	text = review_data['text']
	review_state=evaluate_review(auth_token, \
		book_id,rating,text)
	if 'Succes' in review_state:
		add_review_to_db(review_data)
	return review_state

if __name__ == '__main__':
    app.run(debug=True)
pass





