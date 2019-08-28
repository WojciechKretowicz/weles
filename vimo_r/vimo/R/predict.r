#' @title Make a prediction using **vimo** model
#'
#' @description
#' This tool allows you to make a prediction with model in **vimo**.
#'
#' @param model_name name of the model in **vimo**
#' @X data to make a prediction of, must have named columns, may be path to *.csv* file (must contatin **/** sign) or *hash* of already uploaded data,
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
predict.character <- function(model_name, X, pred_type = 'exact', prepare_columns = TRUE) {
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
		#httr::POST(url = url, body = body)
	} else if(class(X) == "character") {
		# case when X is a path
		body[['is_hash']] =  0
		body[['data']] = httr::upload_file(X)
	} else {
		# case when X is an object
		# creating temporary file

		if(prepare_columns) {
			col = model_info(model_name)$data_info$columns
			columns = rep('a', length(col))
			for(i in 1:length(col)) {
				columns[col[[i]][[1]] + 1] = col[[i]][[2]]
			}
			colnames(X) = columns[-length(col)]
		}

		write.table(X, paste0('./tmp_data_csv-', model_name), row.names=F, col.names=T, sep=',')

		body[['is_hash']] =  0
		body[['data']] = httr::upload_file(paste0('./tmp_data_csv-', model_name))

		# removing temporary file
		del = TRUE
	}

	r = httr::content(httr::POST(url = url, body = body), as='text')

	if(del) {
		file.remove(paste0('./tmp_data_csv-', model_name))
	}
	read.csv(text = r, header = F)[,1]
}
