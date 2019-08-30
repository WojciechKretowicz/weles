#' @title Upload model to **vimo**
#'
#' @description
#' This tool allows you to upload your *mlr* model to model governance base **vimo**.
#'
#' @param model mlr learner, or path to the mlr model written as '.RDS' file
#' @param model_name name of the model that will be visible in the **vimo**
#' @param model_desc description of the model
#' @param tags vector of model's tags, should be vector of strings
#' @param train_dataset training dataset with named columns and target column as the last one, or path to *.csv* file (must contain **/** sign) or hash of already
#' uploaded data
#' @param train_dataset_name name of the training dataset that will be visible in the database
#' @param dataset_desc description of the dataset
#' @param your user name
#' @param password your password
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' \code{
#' library("vimo")
#' library("mlr")
#'
#' task = makeClassifTask(data = iris, target = 'Species')
#' model = makeLearner("classif.randomForest")
#' model = train(model, task)
#'
#' upload(model, "example_model", "This is an example model", c('example', 'easy'), iris, "example_training_data", 'This is an example data', 'Example user', 
#' 'example password')
#' }
#'
#' @export
upload <- function(model, model_name, model_desc, tags, train_dataset, train_dataset_name, dataset_desc, user_name, password) {

	h = digest::digest(c(model_name, model_desc, tags, train_dataset_name, dataset_desc, user_name, password))

	if(!grepl('^[a-z0-9A-Z]+$', model_name)) {
		return("Your model's name contains non alphanumerical characters")
	}

	ses = sessionInfo()
	pkg = c(ses$otherPkgs, ses$loadedOnly)

	pkg_names = rep('a', length(pkg))
	pkg_versions = rep('a', length(pkg))

	for(i in 1:(length(pkg))) {
		pkg_names[i] = names(pkg[i])
		pkg_versions[i] = pkg[[i]]$Version
	}

	requirements = data.frame(pkg_names, pkg_versions)
	write.table(requirements, paste0('.tmp_requirements_', h, '.txt'), row.names=F, col.names=F, sep=',')

	system = Sys.info()[1]
	system_release = Sys.info()[2]
	distribution = strsplit(ses[[4]], split = ' ')[[1]][1]
	distribution_version = strsplit(ses[[4]], split = ' ')[[1]][2]
	language = 'r'
	language_version = paste0(sessionInfo()[[1]]$major, '.', sessionInfo()[[1]]$minor)
	architecture = strsplit(ses[[1]]$system, ', ')[[1]][1]
	processor = Sys.info()[5]

	is_sessionInfo = 1

	del_model = F
	del_train_data = F

	# uploading model
	if(class(model) == "character") {
		# case when model is a path
		body = list('model' = httr::upload_file(model))
	} else {
		# case when model is an object

		# creating temporary file
		saveRDS(model, paste0('.tmp_model_', h, '.rds'))

		# uploading model
		body = list('model' = httr::upload_file(paste0('.tmp_model_', h, '.rds')))

		# setting flag
		del_model = T
	}

	# uploading train dataset
	if(class(train_dataset) == "character" && !grepl("/", train_dataset)) {
		# case when train_dataset is a hash of already uploaded dataset
		body[['train_dataset_hash']] = train_dataset
	} else if(class(train_dataset) == "character") {
		# case when train_dataset is a path to dataset

		body[['train_dataset']] <- httr::upload_file(train_dataset)

		body[['train_dataset_hash']] = 0
	} else {
		# case when train_dataset is a matrix

		# creating temporary file
		write.table(train_dataset, paste0('.tmp_train_data_', h, '.csv'), col.names=T, row.names=F, sep=',')

		# uploading dataset
		body[['train_dataset']] = httr::upload_file(paste0('.tmp_train_data_', h, '.csv'))
		body[['train_dataset_hash']]= 0

		# setting flag
		del_train_data = T
	}

	if(class(model_desc) == 'character' && grepl("/", model_desc)) {
		body[['model_desc']] = paste0(readLines(model_desc), collapse='')
	} else if(class(model_desc) == 'character') {
		body[['model_desc']] = model_desc
	}

	if(class(dataset_desc) == 'character' && grepl("/", dataset_desc)) {
		body[['dataset_desc']] = paste0(readLines(dataset_desc), collapse='')
	} else if(class(dataset_desc) == 'character') {
		body[['dataset_desc']] = dataset_desc
	}
		

	# uploading requirements file
	body[['requirements']] = httr::upload_file(paste0('.tmp_requirements_', h, '.txt'))

	# uploading sessionInfo
	body[['is_sessionInfo']] = 1
	saveRDS(ses, paste0('.tmp_ses_', h, '.rds'))
	body[['sessionInfo']] = httr::upload_file(paste0('.tmp_ses_', h, '.rds'))

	body[['model_name']] = model_name
	body[['system']] = system
	body[['system_release']] = system_release
	body[['distribution']] = distribution
	body[['distribution_version']] = distribution_version
	body[['language']] = language
	body[['language_version']] = language_version
	body[['architecture']] = architecture
	body[['processor']] = processor

	body[['train_data_name']] = train_dataset_name

	body[['user_name']] = user_name
	body[['password']] = password

	tags = as.list(tags)
	names(tags) = rep('tags', length(tags))
	body = c(body, tags)

	r = httr::POST(url = 'http://192.168.137.64/models/post', body = body)

	# removing temporary files
	if(del_model) {
		file.remove(paste0('.tmp_model_', h, '.rds'))
	}
	if(del_train_data) {
		file.remove(paste0('.tmp_train_data_', h, '.csv'))
	}

	file.remove(paste0('.tmp_ses_', h, '.rds'))
	file.remove(paste0('.tmp_requirements_', h, '.txt'))

	httr::content(r, 'text')
}

