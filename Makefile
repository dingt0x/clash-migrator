.PHONY: help
help: ## 帮助信息
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.PHONY: test  dependency dependency-dev dependency-prod deploy deploy-dev dependency-prod

dependency-dev: ## 安装开发依赖到环境中
	@bash ./scripts/dependency.sh  install_dependency_dev

dependency-prod: ## 安装生产依赖到vendor
	@bash ./scripts/dependency.sh  install_dependency_prod

dependency: dependency-dev dependency-prod

test: ## 测试
	@pytest -v

deploy: dependency-prod test ## 部署，默认部署到test环境
	@bash ./scripts/deploy.sh test-env
	@echo "🎉 Deployment successful"

deploy-dev: deploy ## 部署到test环境

deploy-prod: dependency-prod test ## 部署到生成环境
	@bash ./scripts/deploy.sh prod-env
	@echo "🎉 Deployment successful"

