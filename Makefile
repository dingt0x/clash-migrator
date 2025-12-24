.PHONY: help
help: ## 帮助信息
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.PHONY: test deploy update convert

dependency-dev: ## 安装开发依赖到环境中
	@bash ./scripts/dependency.sh  install_dependency_dev

dependency-prod: ## 安装生产依赖到vendor
	@bash ./scripts/dependency.sh  install_dependency_prod

dependency: dependency-dev dependency-prod

test: ## 测试
	@pytest -v

deploy: test
	@bash ./scripts/deploy.sh
	@echo "🎉 Deployment successful"

