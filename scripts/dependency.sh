#!/usr/bin/env bash

set -e
cwd=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
project_path=$(dirname "${cwd}")
lock_file_dev="${project_path}/requirements.dev.lock"
lock_file_prod="${project_path}/requirements.prod.lock"
pyproject_toml="${project_path}/pyproject.toml"
vendor_path="${project_path}/vendor"

compile-dev() {
    uv pip compile "${pyproject_toml}" --extra dev -o "${lock_file_dev}" >/dev/null
}

compile-prod() {
    uv pip compile "${pyproject_toml}" -o "${lock_file_prod}" >/dev/null
}

uv_sync_dev() {
    compile-dev
    if [[ -f "$lock_file_dev" ]]; then
        uv pip sync "$lock_file_dev"
    else
        echo "错误: 未找到 ${lock_file_dev}"
        exit 1
    fi
}

uv_sync_prod() {
    compile-prod
    if [[ -f "$lock_file_prod" ]]; then
        uv pip sync "${lock_file_prod}" --target "$vendor_path"
    else
        echo "错误: 未找到 ${lock_file_dev}"
        exit 1
    fi
}

pip_dev() {
    if [ -z "$lock_file_dev" ]; then
        echo "错误：未找到 ${lock_file_dev} 文件"
        exit 1
    fi
    python pip install -r "${lock_file_dev}"

}

pip_prod() {
    if [ -z "$lock_file_prod" ]; then
        echo "错误：未找到 ${lock_file_prod} 文件"
        exit 1
    fi
    python -m pip install -r "${lock_file_prod}" --target "${vendor_path}"
}

check_venv() {
    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo "⚠️  当前不在 Python 虚拟环境中"
        read -r -p "是否继续？(y/N): " confirm
        case "$confirm" in
        [Yy]*)
            return 0
            ;;
        *)
            exit 1
            ;;
        esac
    fi
    return 0
}

check_uv() {
    if command -v uv >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}


install_dependency_dev(){
    check_venv
    if check_uv; then
        uv_sync_dev
    else
        pip_dev
    fi
}

install_dependency_prod(){
    check_venv
    if check_uv; then
        uv_sync_prod
    else
        pip_prod
    fi
}

main(){
    if [ "$#" -eq "0" ]; then
        echo "Usage: $0 <command> [args1|args2|...]"
        exit
    fi
    local exec_command="$1"
    shift
    "${exec_command}" "$@"
}

main "$@"