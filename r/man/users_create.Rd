% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/users_create.r
\name{users_create}
\alias{users_create}
\title{Create user in the weles}
\usage{
users_create(mail)
}
\arguments{
\item{mail}{your mail, character}
}
\value{
Information if creating an account was successful.
}
\description{
This function is used to create an user account. You need this to have an access to all features in weles.
}
\examples{
\\code{
library("weles")

users_create("Example user", "example password", "example_mail@gmail.com")
}

}
\references{
\href{http://192.168.137.64/models}{\bold{models}}
\href{http://192.168.137.64/datasets}{\bold{datasets}}
}
