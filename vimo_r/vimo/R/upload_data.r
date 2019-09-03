#' @title Get an info about the model in **vimo**
#'
#' @description
#' This tool is used for getting a meta data about the model that is already uploaded to **vimo**.
#'
#' @param model_name Name of the model in **vimo**, character
#'
#' @return named list containing all meta data about model
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' library("vimo")
#'
#' model_info("example_model")
#' model_info("example_model")$model_info
#' model_info("example_model")$data_info
#' model_info("example_model")$data_info$dataset_id
#'
#' @export
upload_data = function(data, data_name, user_name, password) {
	body = list(data_name = data_name, user_name = user_name, password = password)
	h = digest::digest(c(data_name, user_name, password, Sys.time()))
	del_data = F
	if(class(train_dataset) == "character") {
		# case when data is a path to dataset

		body[['data']] <- httr::upload_file(data)
	} else {
		# case when train_dataset is a matrix

		# creating temporary file
		write.table(train_dataset, paste0('.tmp_data_', h, '.csv'), col.names=T, row.names=F, sep=',')

		# uploading dataset
		body[['data']] = httr::upload_file(paste0('.tmp_data_', h, '.csv'))

		# setting flag
		del_data = T
	}
	r = httr::content(httr::POST(url = 'http://192.168.137.64/datasets/post'), 'text')

	if(del_data) {
		file.remove(paste0('.tmp_data_', h, '.csv'))
	}

	r
}
