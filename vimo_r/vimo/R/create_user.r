#' @title Get an info about the model in **vimo**
#'
#' @description
#' Thanks to this function you can create user on **vimo**.
#'
#' @param user_name your user name in **vimo**, character
#' @param password your password, character
#' @param mail your password, character
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
create_user = function(user_name, password, mail) {
	body = list('user_name' = user_name, 'password' = password, 'mail' = mail)
	httr::content(httr::POST('http://192.168.137.64/users/create_user', body=body))
}
