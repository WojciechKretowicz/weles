#' @title Make an audit of the model in the vimo
#'
#' @description
#' You can use this function to audit in different ways models already uploaded in the vimo.
#'
#' @param model_name name of the model in the vimo, character
#' @param measure name of the measure used in the audit, character
#' @param user your user name, character
#' @param password your password
#' @param data data frame to make an audit on or path or hash of already uploaded dataset
#' @param target name of the target column in the dataset
#' @param data_name name of the dataset that will be visible in the vimo, unnecessary if data is a hash
#' @param data_desc description of the dataset, unnecessary if data is a hash
#'
#' @return result of the audit or information if somethin went wrong
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' \code{
#' library("vimo")
#'
#' model_audit('example_model', 'mae', 'Example user', 'example password', iris, 'Species', 'iris', 'Flowers')
#' model_audit('example_model', 'acc', 'Example user', 'example password', 'aaaaaaaaaaaaaaaaaaaaaaaaaa', 'Species')
#' }
#'
#' @export
model_audit = function(model_name, measure, user, password, data, target, data_name=NA, data_desc=NA) {

	# checking input
	stopifnot(class(model_name) == 'character')
	stopifnot(class(measure) == 'character')
	stopifnot(class(user) == 'character')
	stopifnot(class(password) == 'character')
	stopifnot(class(data) == 'data.frame' || (class(data) == 'character' && nchar(data) == 64 && !is.na(data_name) && !is.na(data_desc)))
	stopifnot(class(target) == 'character')
	stopifnot(is.na(data_name) || class(data_name) == 'character')
	stopifnot(is.na(data_desc) || class(data_desc) == 'character')

	# making the body for the request
	info = list('model_name'= model_name, 'measure'= measure, 'user'= user, 'password'= password, 'target'= target)

	# creating hash for the temporary files
	h = digest::digest(Sys.time())

	# flag
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

		# setting the flag
		del_data = TRUE

		# uploading
		r = httr::POST('http://192.168.137.64/models/audit', body=info)
	}

	if (del_data) {
		# case when there was temporary data file
		file.remove(paste0('.tmp_data_', h, '.csv'))
	}

	# return
	httr::content(r, 'text')
}
