
def formatare_csv(new_account):
	formatted_csv='';
	for key in new_account:
		formatted_csv+=str(new_account[key])+';';
	formatted_csv+='\n'
	return formatted_csv
