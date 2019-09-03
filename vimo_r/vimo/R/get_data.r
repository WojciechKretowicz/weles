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
	httr::GET(paste0('http://192.168.137.64/datasets/', dataset_id))
}
