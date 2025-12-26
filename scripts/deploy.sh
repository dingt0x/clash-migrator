#!/usr/bin/env bash

#!/usr/bin/env bash

# 设置错误时退出
set -e

check_env(){
    read -r -p "Deploy to prod?<Y/N> " confirm
    case "$confirm" in
        [Yy]*)
            return 0
            ;;
        *)
            exit 1
            ;;
        esac
}

ENV="${1:-""}"
if [ "${ENV}" == "prod-env" ]; then
    check_env
    LAMBDA_FUNCTION_NAME="clashx"
elif [ "${ENV}" == "test-env" ]; then
    LAMBDA_FUNCTION_NAME="clashx-test"
else
    echo "Usage: $0 <env: test-env/prod-env>"
    exit 1
fi


export AWS_PROFILE="dtw"
export AWS_REGION="ap-northeast-1"
repo_base_dir=$(git rev-parse --show-toplevel 2> /dev/null)
cache_dir="${repo_base_dir}/.cache"
lambda_dir="${repo_base_dir}/."
lambda_zip_dir="${cache_dir}/lambda"
zip_file="${lambda_zip_dir}/lambda-deployment.zip"
echo "开始部署Lambda函数: ${LAMBDA_FUNCTION_NAME}"

mkdir -p "${lambda_zip_dir}"

if [ -f "${zip_file}" ]; then
    echo "删除旧的部署包..."
    rm "${zip_file}"
fi

cd "$lambda_dir" ||  { echo "$lambda_dir 不存在";exit 1; }

echo "创建部署包..."
zip -r "${zip_file}" src/ templates/ vendor/ \
    -x "*.git*" \
    -x "*.cache*" \
    -x "*.vscode*" \
    -x "*.DS_Store*" \
    -x "README.md" \
    -x "*.sh" \
    -x ".env*" \
    -x "node_modules/*" \
    -x "venv/*" \
    -x "__pycache__/" \
    -x "*.pyc" \
    -x "tests/*" \
    -x "docs/*" > /dev/null

echo "部署包创建完成: ${zip_file}"

echo -n "Update functon config ... "
aws lambda update-function-configuration \
    --function-name  "${LAMBDA_FUNCTION_NAME}" \
    --handler 'src.lambda_function.lambda_handler' \
    --timeout 30 \
    --no-cli-pager --output json > /dev/null
echo "✅  "

# 更新Lambda函数代码
echo -n "更新 Lambda函数 ${LAMBDA_FUNCTION_NAME} ... "
aws lambda update-function-code \
    --function-name "${LAMBDA_FUNCTION_NAME}" \
    --zip-file "fileb://${zip_file}" \
    --no-cli-pager  --output json  > /dev/null
echo "✅  "

#if [ $? -eq 0 ]; then
#    echo "✅ Lambda函数 ${LAMBDA_FUNCTION_NAME} 更新成功！"
#
#    # --profile "${AWS_PROFILE}" \
#    # --region "$REGION" \
#    # 获取更新后的函数信息
#    echo "获取函数信息..."
#    aws lambda get-function \
#        --function-name "${LAMBDA_FUNCTION_NAME}" \
#        --query 'Configuration.[FunctionName,Runtime,LastModified,CodeSize]' \
#        --no-cli-pager \
#        --output json
#else
#    echo "❌ Lambda函数更新失败"
#    exit 1
#fi



echo -n "Publish version ... "
aws lambda publish-version \
    --function-name "${LAMBDA_FUNCTION_NAME}" \
    --no-cli-pager  --output json || true  > /dev/null
echo "✅  "


echo "部署完成！"
