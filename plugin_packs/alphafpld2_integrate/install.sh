#!/bin/bash

# referenced from https://github.com/YoshitakaMo/localcolabfold/tree/main

install_colabfold() {
    echo "Starting ColabFold installation..."

    if ! command -v conda &> /dev/null; then
        echo "Error: conda command not found. Please install Conda first."
        exit -1
    fi
    CONDA_BASE="$(conda info --base)"

    conda create -n colabfold -c conda-forge -c bioconda\
        python=3.13 kalign2=2.04 hhsuite=3.3.0\
        mmseqs2=18.8cc5c -y
    source "$CONDA_BASE/etc/profile.d/conda.sh"
    conda activate colabfold
    pip install colabfold[alphafold,openmm] jax[cuda] openmm[cuda12]
    ## Download weights
    python -m colabfold.download

    CONDA_BASE="$(conda info --base)"
    mkdir -p "$HOME/.local/bin"
    if [[ ! $PATH =~ "$HOME/.local/bin" ]]; then
        echo "export PATH=\$PATH:\$HOME/.local/bin" >> "$HOME/.bashrc"
    fi
    ln -s "$CONDA_BASE/envs/colabfold/bin/colabfold_batch" "$HOME/.local/bin/colabfold_batch"
    echo "Installation of ColabFold finished."
}

# Check if colabfold_batch command exists
if ! command -v colabfold_batch &> /dev/null; then
    echo "Error: colabfold_batch command not found"
    read -p "Do you want to install ColabFold? (y/n): " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        install_colabfold
    else
        echo "Installation cancelled."
        exit -1
    fi
fi

exit 0
