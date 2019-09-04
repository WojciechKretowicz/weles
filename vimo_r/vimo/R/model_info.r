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
model_info = function(model_name) {
	content = httr::content(httr::GET(url = paste0('http://192.168.137.64/models/', model_name, '/info')))

	audits = content$audits

	auds = list()
	for(name in names(audits)) {
		v = c()
		v[as.numeric(names(unlist(audits[[name]])))+1] = unlist(audits[[name]])
		auds[[name]] = v
	}

	columns = content$columns

	cols = list()
	for(name in names(columns)) {
		v = c()
		v[as.numeric(names(unlist(columns[[name]])))+1] = unlist(columns[[name]])
		cols[[name]] = v
	}
	
	list(model = content$model, data = content$data, audits = data.frame(auds), columns = data.frame(cols))
}
