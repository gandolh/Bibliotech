from checking_authentication import already_exist
from auth_tokens_generators import encode_auth_token as enc_at,\
    decode_auth_token as dec_at
from formating_text import formatare_csv
def evaluate_review(auth_token, book_id,rating,text):
	email=dec_at(auth_token)
	if not already_exist(str(email),filename='databases/accounts_db.csv'):
		return {
		'errorMessage':'Sorry, but this token is expired'
		}
	if not already_exist(str(book_id),filename='databases/books_db.csv'):
		return{
		'errorMessage':'Sorry,but this book does not exist'
		}
	if rating not in (1,5):
		return{
		'errorMessage':'Please insert a number between 1 and 5'
		}
	return {
	'Succes': 'Review added succesfully'
	}

def add_review_to_db(review_data):
	to_print_data=review_data.copy()
	to_print_data['author']=dec_at(to_print_data['auth_token'])
	to_print_data.pop('auth_token')
	with open('databases/reviews_db.csv','a+') as fl:
		fl.write(formatare_csv(to_print_data))

def get_rating(book_id):
	rating=0;
	no_ratings=0;
	with open('databases/reviews_db.csv','r') as fl:
		line=fl.readline();
		while line:
			lazy_list=line.split(';')
			if str(lazy_list[0])==str(book_id):
				rating+=int(lazy_list[1])
				no_ratings+=1
			line=fl.readline()
	if rating==0:
		return rating
	else: return rating/ no_ratings


def get_list_of_reviews(b_id):
	list_of_reviews=[];
	with open('databases/reviews_db.csv','r') as fl:
		line=fl.readline()
		while line:
			lazy_list=line.split(';')
			if str(lazy_list[0])==str(b_id):
				list_of_reviews.append({
					'rating':lazy_list[1],
					'review':lazy_list[2],
					'author':lazy_list[3]
					})
			line=fl.readline()
	return list_of_reviews


if __name__ == '__main__':
    auth_tok='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM4MzM4MDksImlhdCI6MTYxMzc0NzQwOSwic3ViIjoiaW5jYW1lcmdlQGluY2FwdXRpbi5jb20ifQ.uP_DjrA1OyPnMfb9eoVfxtZpwR8nqIWTlDegW14cSW8'
    # evaluate_review(auth_tok,2,5,'some text here')