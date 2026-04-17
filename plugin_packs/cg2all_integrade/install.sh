#!/bin/bash

install_cg2all() {
    echo "Starting cg2all installation..."
    if ! command -v conda &> /dev/null; then
        echo "Error: conda command not found. Please install Conda first."
        exit -1
    fi
    CONDA_BASE="$(conda info --base)"

    if ! command -v git &> /dev/null; then
        echo "Error: git command not found. Please install git first."
        exit -1
    fi

    # Check if github is accessible
    if curl -s --max-time 3 https://github.com &> /dev/null; then
        GITHUB_PROXY_URL=""
    else
        GITHUB_PROXY_URL="https://gh-proxy.com/"
    fi

    # Check if huggingface is accessible
    if curl -s --max-time 3 https://huggingface.co &> /dev/null; then
        HF_ENDPOINT="https://huggingface.co"
    else
        HF_ENDPOINT="https://hf-mirror.com"
    fi
    conda create --name cg2all python=3.11 cudatoolkit dgl=1.0 -c dglteam/label/cu113 -y

    source "$CONDA_BASE/etc/profile.d/conda.sh"
    conda activate cg2all

    TMP_DIR="$(mktemp -d /tmp/cg2all.XXXXXX)"
    trap 'rm -rf "$TMP_DIR"' EXIT

    pushd "$TMP_DIR"
    git clone --depth 1 --single-branch "${GITHUB_PROXY_URL}https://github.com/huhlim/mdtraj" mdtraj
    pushd mdtraj
        pip install .
    popd
    git clone --depth 1 --single-branch "${GITHUB_PROXY_URL}https://github.com/huhlim/SE3Transformer" se3-transformer
    pushd se3-transformer
        pip install .
    popd
    git clone --depth 1 --single-branch "${GITHUB_PROXY_URL}https://github.com/huhlim/cg2all" cg2all
    pushd cg2all
        sed -i 's/^torch = ".*"/torch = "2.11"/' pyproject.toml
        sed -i 's#^mdtraj = {git = "https://github.com/huhlim/mdtraj.git"}#mdtraj = "0+untagged.1.g05907b1"#' pyproject.toml
        sed -i 's#^se3_transformer = {git = "https://github.com/huhlim/SE3Transformer.git"}#se3_transformer = "0.1.2"#' pyproject.toml
        pip install .
    popd
    popd
    MODEL_PATH="$CONDA_BASE/envs/cg2all/lib/python3.11/site-packages/cg2all/model"
    mkdir -p "$MODEL_PATH"
    wget -O "$MODEL_PATH/CalphaBasedModel.ckpt" \
        "$HF_ENDPOINT/spaces/huhlim/cg2all/resolve/main/model/CalphaBasedModel.ckpt"
    mkdir -p "$HOME/.local/bin"
    if [[ ! $PATH =~ "$HOME/.local/bin" ]]; then
        echo "export PATH=\$PATH:\$HOME/.local/bin" >> "$HOME/.bashrc"
    fi
    ln -s "$CONDA_BASE/envs/cg2all/bin/convert_cg2all" "$HOME/.local/bin/convert_cg2all"
    echo "Installation of cg2all finished."
}

# Check if colabfold_batch command exists
if ! command -v convert_cg2all &> /dev/null; then
    echo "Error: convert_cg2all command not found"
    read -p "Do you want to install cg2all? (y/n): " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        install_cg2all
    else
        echo "Installation cancelled."
        exit -1
    fi
fi

exit 0
