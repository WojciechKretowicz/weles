#' @title Upload the dataset to the vimo
#'
#' @description
#' This function uploads the dataset and needed metadata to the vimo.
#'
#' @param data the data frame to upload or path
#' @param data_name name of the dataset that will be visible in the vimo
#' @param data_desc description of the dataset
#' @param user_name your user name
#' @param password your password
#'
#' @return information if uploading the data was successful
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' library("vimo")
#'
#' upload_data(X, 'data name', 'Example user', 'example password')
#'
#' @export
data_upload = function(data, data_name, data_desc, user_name, password) {

	#stopifnot(class(data) == 'data.frame' || class(data) == 'character')
	stopifnot(class(data_name) == 'character')
	stopifnot(class(data_desc) == 'character')
	stopifnot(class(user_name) == 'character')
	stopifnot(class(password) == 'character')

	# making the for the request
	body = list(data_name = data_name, data_desc = data_desc, user_name = user_name, password = password)

	# making the hash for the temporary files
	h = digest::digest(c(data_name, user_name, password, Sys.time()))

	# setting flag
	del_data = FALSE

	if(class(data) == "character") {
		# case when data is a path to dataset

		body[['data']] <- httr::upload_file(data)
	} else {
		# case when dataset is a matrix

		# creating temporary file
		write.table(data, paste0('.tmp_data_', h, '.csv'), col.names=T, row.names=F, sep=',')

		# uploading dataset
		body[['data']] = httr::upload_file(paste0('.tmp_data_', h, '.csv'))

		# setting flag
		del_data = T
	}

	# uploading data
	r = httr::content(httr::POST(url = 'http://192.168.137.64/datasets/post', body=body), 'text')

	if(del_data) {
		# if there was temporary data file

		file.remove(paste0('.tmp_data_', h, '.csv'))
	}

	# return
	r
}