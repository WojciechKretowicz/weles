#' @title Create user in the vimo
#'
#' @description
#' This function is used to create an user account. You need this to have an access to all features in vimo.
#'
#' @param user_name your user name in **vimo**, character
#' @param password your password, character
#' @param mail your mail, character
#'
#' @return Information if creating an account was successful.
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' \code{
#' library("vimo")
#'
#' create_user("Example user", "example password", "example_mail@gmail.com")
#' }
#'
#' @export
audit_model = function(model_name, measure, user, password, data, target, data_name=NA, data_desc=NA) {

	info = list('model_name'= model_name, 'measure'= measure, 'user'= user, 'password'= password, 'target'= target)

	h = digest::digest(Sys.time())

	del_data = FALSE

	# uploading data
	if (class(data) == 'character' && !grepl('/', data)) {
		# case when data is a hash
		info[['is_hash']] = 1
		info[['hash']] = data

		r = httr::POST('http://192.168.137.64/models/audit', body=info)
	} else if (class(data) == 'character') {
		# case when data is a path
		info[['is_hash']] = 0
		info[['data_name']] = data_name
		info[['data_desc']] = data_desc
		info[['data']] = upload_file(data)

		r = httr::POST('http://192.168.137.64/models/audit', body=info)
	} else {
		# case when data is an object

		info[['is_hash']] = 0
		info[['data_name']] = data_name
		info[['data_desc']] = data_desc

		# creating temporary file
		write.table(data, paste0('.tmp_data_', h, '.csv'), col.names=T, row.names=F, sep=',')

		info[['data']] = upload_file(paste0('.tmp_data_', h, '.csv'))

		del_data = TRUE

		r = httr::POST('http://192.168.137.64/models/audit', body=info)
	}

	if (del_data) {
		file.remove(paste0('.tmp_data_', h, '.csv'))
	}
	httr::content(r, 'text')
}
