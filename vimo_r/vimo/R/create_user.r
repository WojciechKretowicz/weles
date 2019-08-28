#' @title Create user in the vimo
#'
#' @description
#' This function is used to create an user account. You need this to have an access to all features in vimo.
#'
#' @param user_name your user name in **vimo**, character
#' @param password your password, character
#' @param mail your mail, character
#'
#' @return Information if creating an account was successful.
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' \code{
#' library("vimo")
#'
#' create_user("Example user", "example password", "example_mail@gmail.com")
#' }
#'
#' @export
create_user = function(user_name, password, mail) {
	body = list('user_name' = user_name, 'password' = password, 'mail' = mail)
	httr::content(httr::POST('http://192.168.137.64/users/create_user', body=body))
}
