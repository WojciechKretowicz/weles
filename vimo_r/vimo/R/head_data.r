#' @title Get the head of the dataset in the vimo
#'
#' @description
#' This tool allows you to view the head of the dataset in the vimo.
#'
#' @param dataset_id the dataset hash
#' @param n number of rows to show
#'
#' @return top n rows of the dataset
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' library("vimo")
#'
#' head_data('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#'
#' @export
head_data = function(dataset_id, n=5) {
	httr::POST(paste0('http://192.168.137.64/datasets/', dataset_id), body = list('n' = n))
}
