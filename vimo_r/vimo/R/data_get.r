#' @title Get the dataset from **vimo**
#'
#' @description
#' You can use this function to download the dataset from vimo as a data frame
#'
#' @param dataset_id hash of the dataset
#'
#' @return data frame
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' library("vimo")
#'
#' get_data('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#'
#' @export
data_get = function(dataset_id) {

	# checking input
	stopifnot(class(dataset_id) == 'character')
	stopifnot(nchar(dataset_id) == 64)

	# getting dataset	
	df = httr::content(httr::GET(paste0('http://192.168.137.64/datasets/', dataset_id)), 'parsed')

	# formatting
	cols = list()
	for(name in names(df)) {
		v = c()
		v[as.numeric(names(unlist(df[[name]])))+1] = unlist(df[[name]])
		cols[[name]] = v
	}

	# return
	data.frame(cols)
}
