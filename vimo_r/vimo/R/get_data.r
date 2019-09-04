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
get_data = function(dataset_id) {
	df = httr::content(httr::GET(paste0('http://192.168.137.64/datasets/', dataset_id)), 'parsed')
	cols = list()
	for(name in names(df)) {
		v = c()
		v[as.numeric(names(unlist(df[[name]])))+1] = unlist(df[[name]])
		cols[[name]] = v
	}
	data.frame(cols)
}
