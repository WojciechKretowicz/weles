predict <- function(model_name, X, pred_type = 'exact') {
	# url
	url = paste0('http://192.168.137.64/models/', model_name, '/predict/', pred_type)

	body = list()

	del = FALSE

	# uploading data
	if(class(X) == "character" && !grepl("/", X)) {
		# case when X is a hash
		body[['is_hash']] =  1
		body[['hash']] = X

		# request
		POST(url = url, body = body)
	} else if(class(X) == "character") {
		# case when X is a path
		body[['is_hash']] =  0
		body[['data']] = upload_file(X)
	} else {
		# case when X is an object
		# creating temporary file
		write.table(X, paste0('./tmp_data_csv-', model_name), row.names=F, col.names=T, sep=',')

		body[['is_hash']] =  0
		body[['data']] = upload_file(paste0('./tmp_data_csv-', model_name))

		# removing temporary file
		del = TRUE
	}

	r = content(POST(url = url, body = body), as='text')

	if(del) {
		file.remove(paste0('./tmp_data_csv-', model_name))
	}
	read.csv(text = r, header = F)[,1]
}
