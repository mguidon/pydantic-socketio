.DEFAULT_GOAL := help

.PHONY: create_models

create_models: ## create pydantic models from spec file
	python parser/parse_asyncapi.py --spec_file=specs/async-api.yml --template_file=specs/template.yml --model_file=model/model.py

.venv: ## creating virtual environment
	@python3 -m venv $@
	# updating package managers
	@$@/bin/pip --no-cache install --upgrade \
		pip \
		setuptools \
		wheel
	@$@/bin/pip --no-cache install -r requirements.txt
	
# MISC ---------------------------------------------------------------

.PHONY: help
help: ## help on rule's targets
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
