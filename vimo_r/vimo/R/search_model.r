#' @title Find model that interests you the most
#'
#' @description
#' Function finds all models having at least one common tag with those passed as the argument
#'
#' @param tags vector of tags, should be strings
#'
#' @return vector of models' names that have at least one common tag with those passed as the argument
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' \code{
#' library("vimo")
#'
#' search_model(c('example', 'easy'))
#' }
#'
#' @export
search_model = function(tags) {
	tags = as.list(tags)
	names(tags) = rep('tags', length(tags))
	result = httr::content(httr::POST(url = 'http://192.168.137.64/models/search', body = tags))
	unlist(result$models)
}
