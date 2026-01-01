#!/usr/bin/env bash
set -euo pipefail

export AWS_REGION="ap-northeast-1"
export AWS_PROFILE="dtw"

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 <LAMBDA_NEM> <ENV_NAME> <ENV_VALUE>"
    exit 1
fi

LAMBDA_NAME="$1"
ENV_KEY="$2"
ENV_VALUE="$3"

update_env() {
    if [[ $# -ne 1 ]]; then
        echo "Usage: $0 <lambda_name>"
        return 1
    fi

    local lambda_name
    lambda_name="$1"

    BEFORE_ENV_JSON=$(aws lambda get-function-configuration \
        --function-name "$lambda_name" \
        --region "$AWS_REGION" \
        --query 'Environment.Variables' \
        --output json)

    if [[ "$BEFORE_ENV_JSON" == "null" ]]; then
        BEFORE_ENV_JSON="{}"
    fi
    AFTER_ENV_JSON=$(echo "$BEFORE_ENV_JSON" |
        jq -c --arg k "$ENV_KEY" --arg v "$ENV_VALUE" '. + {($k): $v}')

    BEFORE_SORTED=$(echo "$BEFORE_ENV_JSON" | jq -S .)
    AFTER_SORTED=$(echo "$AFTER_ENV_JSON" | jq -S .)

    echo "====== BEFORE ======"
    echo "$BEFORE_ENV_JSON" | jq .
    echo

    if [[ "$BEFORE_SORTED" == "$AFTER_SORTED" ]]; then
        echo "ℹ️ No changes detected. Nothing to update."
        return
    fi

    echo "====== AFTER ======"
    echo "$AFTER_ENV_JSON" | jq .
    echo

    echo "====== DIFF ======"
    diff -u \
        <(echo "$BEFORE_ENV_JSON" | jq -S .) \
        <(echo "$AFTER_ENV_JSON" | jq -S .) || true
    echo

    # ====== 确认 ======
    read -r -p "Apply changes to Lambda? [y/N]: " CONFIRM

    case "$CONFIRM" in
    y | Y | yes | YES)
        echo "🚀 Updating lambda environment..."
        aws lambda update-function-configuration \
            --function-name "$lambda_name" \
            --region "$AWS_REGION" \
            --environment "{\"Variables\":$AFTER_ENV_JSON}" \
            >/dev/null
        echo "✅ Lambda environment updated successfully"
        ;;
    *)
        echo "❎ Aborted. No changes applied."
        exit 0
        ;;
    esac

}

update_env "$LAMBDA_NAME"
