#' @title Find model that interests you the most
#'
#' @description
#' Function allows you advanced search of models in vimo. If all parameters are default then returns all models' name in vimo.
#'
#' @param row parameter descibing number of rows in training dataset, '<n;' '>n;' '=n;' '>a;<b'
#' @param column parameter descibing number of columns in training dataset, '<n;' '>n;' '=n;' '>a;<b'
#' @param missing parameter descibing number of missing values in training dataset, '<n;' '>n;' '=n;' '>a;<b'
#' @param classes parameter descibing number of classes in training dataset, '<n;' '>n;' '=n;' '>a;<b'
#' @param owner show only models created by this user
#' @param tags vector of tags, should be all strings
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
#' search_model(tags = c('example', 'easy'))
#'
#' search_model(row='<15000;', tags = c('example', 'easy'))
#'
#' search_model(column='>10;<15;', owner='Example user')
#'
#' search_model(row='>1000;<10000;', column='=14;', classes='=2;', missing='=0;', owner='Example user', tags = c('example', 'easy'), regex='^R')
#' }
#'
#' @export
search_model = function(row=NA, column=NA, missing=NA, classes=NA, owner=NA, tags=c(), regex=NA) {
	body = as.list(tags)
	names(body) = rep('tags', length(body))
	body[['row']] = row
	body[['column']] = column
	body[['missing']] = missing
	body[['classes']] = classes
	body[['owner']] = owner
	body[['regex']] = regex
	result = httr::content(httr::POST(url = 'http://192.168.137.64/models/search', body = body))
	unlist(result$models)
}
