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
#'
#' @export
search_model = function(tags) {
	tags = as.list(tags)
	names(tags) = rep('tags', length(tags))
	result = httr::content(httr::POST(url = 'http://192.168.137.64/models/search', body = tags))
	unlist(result$models)
}
