#' @title Upload model to **vimo**
#'
#' @description
#' This tool is allows you to upload your *mlr* model to model governance base **vimo**.
#'
#' @param model mlr learner, or path to the mlr model written as learner
#' @param model_name name of the model that will be visible in **vimo**
#' @train_dataset training dataset with named columns and target column as the last one, or path to *.csv* file (must contain **/** sign) or hash of already
#' uploaded data
#' @train_dataset_name name of the training dataset that will be visible in the database
#'
#' @references
#' \href{http://192.168.137.64/models}{\bold{models}}
#' \href{http://192.168.137.64/datasets}{\bold{datasets}}
#'
#' @examples
#' library("vimo")
#' library("mlr")
#'
#' task = makeClassifTask(data = iris, target = 'Species')
#' model = makeLearner("classif.randomForest")
#' model = train(model, task)
#'
#' upload(model, "example_model", iris, "example_training_data")
#'
#' @export
upload <- function(model, model_name, train_dataset, train_dataset_name, test_dataset = NA, test_dataset_name = NA) {
	ses = sessionInfo()
	pkg = c(ses$otherPkgs, ses$loadedOnly)

	pkg_names = rep('a', length(pkg))
	pkg_versions = rep('a', length(pkg))

	for(i in 1:(length(pkg))) {
		pkg_names[i] = names(pkg[i])
		pkg_versions[i] = pkg[[i]]$Version
	}

	requirements = data.frame(pkg_names, pkg_versions)
	write.table(requirements, '.tmp-requirements.txt', row.names=F, col.names=F, sep=',')

	system = Sys.info()[1]
	system_release = Sys.info()[2]
	distribution = strsplit(ses[[4]], split = ' ')[[1]][1]
	distribution_version = strsplit(ses[[4]], split = ' ')[[1]][2]
	language = 'r'
	language_version = paste0(sessionInfo()[[1]]$major, '.', sessionInfo()[[1]]$minor)
	architecture = strsplit(ses[[1]]$system, ', ')[[1]][1]
	processor = Sys.info()[5]

	if(is.na(test_dataset)) {
		is_test_dataset = 0
	} else {
		is_test_dataset = 1
	}

	is_sessionInfo = 1

	del_model = F
	del_train_data = F
	del_test_data = F

	# uploading model
	if(class(model) == "character") {
		# case when model is a path
		body = list('model' = upload_file(model))
	} else {
		# case when model is an object

		# creating temporary file
		saveRDS(model, '.tmp_model')

		# uploading model
		body = list('model' = upload_file('.tmp_model'))

		# setting flag
		del_model = T
	}

	# uploading train dataset
	if(class(train_dataset) == "character" && !grepl("/", train_dataset)) {
		# case when train_dataset is a hash of already uploaded dataset
		body[['train_dataset_hash']] = train_dataset
	} else if(class(train_dataset) == "character") {
		# case when train_dataset is a path to dataset
		#body = c(body, list('train_dataset' = upload_file(train_dataset)))

		body[['train_dataset']] <- upload_file(train_dataset)

		#body['traindataset'] = upload_file
		body[['train_dataset_hash']] = 0
	} else {
		# case when train_dataset is a matrix

		# creating temporary file
		write.table(train_dataset, './tmp_train_data_csv', col.names=T, row.names=F, sep=',')

		# uploading dataset
		body[['train_dataset']] = upload_file('./tmp_train_data_csv')
		body[['train_dataset_hash']]= 0

		# setting flag
		del_train_data = T
	}

	# uploading train_dataset
	if(is.na(test_dataset)) {
		# case when test_dataset is not provided
		body[['is_test_dataset']] = 0
		body[['test_dataset_hash']] = 0
	}
	else if(class(test_dataset) == "character" && !grepl("/", test_dataset)) {
		# case when test_dataset is a hash of already uploaded dataset
		body[['test_dataset_hash']] = test_dataset
		body[['is_test_dataset']] = 1
	}
	else if(class(test_dataset) == "character") {
		# case when test_dataset is a path to csv file
		body[['test_dataset']] = upload_file(test_dataset)
		body[['is_test_dataset']] = 1
		body[['is_test_dataset_hash']] = 0
	}
	else {
		# case when test_dataset is a matrix

		# creating temporary file
		write.table(test_dataset, './tmp_train_data_csv', col.names=F, sep=',')

		# uploading dataset
		body[['test_dataset']] = upload_file('tmp_test_data_csv')

		# setting flag
		del_test_data = T
	}

	# uploading requirements file
	body[['requirements']] = upload_file('.tmp-requirements.txt')

	# uploading sessionInfo
	body[['is_sessionInfo']] = 1
	saveRDS(ses, '.tmp-ses')
	body[['sessionInfo']] = upload_file('.tmp-ses')

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
	body[['test_data_name']] = test_dataset_name

	POST(url = 'http://192.168.137.64/models/post', body = body)

	# removing temporary files
	if(del_model) {
		file.remove('.tmp_model')
	}
	if(del_train_data) {
		file.remove('./tmp_train_data_csv')
	}
	if(del_test_data) {
		file.remove('./tmp_test_data_csv')
	}
}

