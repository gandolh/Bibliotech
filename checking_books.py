from auth_tokens_generators import decode_auth_token as dec_at
from checking_authentication import already_exist
from review_methods import get_rating,get_list_of_reviews

def get_book_id():
	with open('databases/books_db.csv','r') as fl:
		line=fl.readline();
		id=line.split(';')[0];
		while line:
			id=line.split(';')[0];
			line=fl.readline();
		# return id
		if id != '':
			return str(int(id)+1)
		else: return 0


def evaluate_add_book(auth_token, book_name, book_author, description):
	email= dec_at(auth_token)
	if already_exist(email,'1',filename='databases/accounts_db.csv')== True:
		if already_exist(book_name,book_author,filename='databases/books_db.csv') == True:
			return{
			'errorMessage': 'sorry bro, this book already exist'
			}
		else:return {
		'id': get_book_id(), #generate id
		'book_name':book_name,
		'book_author':book_author,
		'description': description,
		'status': 'disponibila'
		}
	else: return{
	'errorMessage': 'Invalid credentials'
	}
def get_book_by_id_books(b_id):
	b_id= str(b_id)
	with open('databases/books_db.csv','r') as fl:
		line=fl.readline();
		while line:
			lazy_list=line.split(';')
			if lazy_list[0]== b_id:
				return{
				'id': lazy_list[0],
				'Title': lazy_list[1],
				'Author': lazy_list[2],
				'Description': lazy_list[3]
				}
			# print(lazy_list)
			line=fl.readline()
		return{
		'errorMessage': 'not found'
		}

def evaluate_get_book(b_id,auth_token=None):
	full_book_details=get_book_by_id_books(b_id);
	full_book_details['rating']=get_rating(b_id);
	full_book_details['reviews']=get_list_of_reviews(b_id)
	if auth_token==None:
		for i in full_book_details['reviews']:
			i.pop('author')
	return full_book_details


def evaluate_get_books():
	books_list=[]
	with open('databases/books_db.csv','r') as fl:
		line= fl.readline()
		while line:
			lazy_list=line.split(';')
			books_list.append({
				'id': lazy_list[0],
				'title': lazy_list[1],
				'author': lazy_list[2],
				'description': lazy_list[3],
				'status': lazy_list[4],
				'rating': get_rating(lazy_list[0])

				})
			line=fl.readline()
	if books_list:return {
	'books': books_list
	}
	else:return{
	'errorMessage':'No books in library'
}
if __name__ == '__main__':
	# email = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM2NDYxMjksImlhdCI6MTYxMzU1OTcyOSwic3ViIjoiY2xvcG90ZWwuYWRtaW5AZ21haWwuY29tIn0.l6drFG8gCl8nDDRRnjxs84fS-13gyu5D1pEWWpJmy1M'
	# print(evaluate_add_book(email,'a','a','a'))

	pass