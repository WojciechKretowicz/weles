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
model_info = function(model_name) {
	httr::content(httr::GET(url = paste0('http://192.168.137.64/models/', model_name, '/info')))
}
