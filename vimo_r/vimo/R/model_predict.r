#' @title Make a prediction using vimo model
#'
#' @description
#' This tool allows you to make a prediction with model in vimo.
#'
#' @param model_name name of the model in vimo
#' @param X data to make a prediction of, must have named columns, may be path to *.csv* file (must contatin **/** sign) or *hash* of already uploaded data,
#' if X is an object and prepare_columns is True, columns' names will be fetched automatically
#' @param pred_type type of prediction, 'exact' or 'prob'
#' @param prepare_columns if X is an object then columns' names will be fetched automatically
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' \code {
#' library("vimo")
#'
#' predict("example_model", iris[,-5])
#' }
#'
#' @export
model_predict <- function(model_name, X, pred_type = 'exact', prepare_columns = TRUE) {

	# checking input
	stopifnot(class(model_name) == 'character')
	stopifnot(class(X) == 'data.frame' || class(X) == 'character')
	stopifnot(class(pred_type) == 'character')
	stopifnot(class(prepare_columns) == 'logical')

	# making the hash for temporary files
	h = digest::digest(c(model_name, Sys.time()))

	# url
	url = paste0('http://192.168.137.64/models/', model_name, '/predict/', pred_type)

	# body for the request
	body = list()

	# flag telling if delete file
	del = FALSE

	# uploading data
	if(class(X) == "character" && !grepl("/", X)) {
		# case when X is a hash
		body[['is_hash']] =  1
		body[['hash']] = X

	} else if(class(X) == "character") {
		# case when X is a path
		body[['is_hash']] =  0
		body[['data']] = httr::upload_file(X)
	} else {
		# case when X is an object

		# fetching columns
		if(prepare_columns) {
			info = model_info(model_name)
			columns = info$columns
			target = info$model$target
			columns = columns[order(columns$id), 'name']
			columns = columns[columns != target]
			names(X) = columns
		}

		# creating temporary file
		write.table(X, paste0('.tmp_data_', h, '.csv'), row.names=F, col.names=T, sep=',')

		body[['is_hash']] =  0
		body[['data']] = httr::upload_file(paste0('.tmp_data_', h, '.csv'))

		# removing temporary file
		del = TRUE
	}

	# uploading
	r = httr::content(httr::POST(url = url, body = body), as='text')

	# deleting temporary files
	if(del) {
		file.remove(paste0('.tmp_data_', h, '.csv'))
	}

	# return
	read.csv(text = r, header = F)[,1]
}
