# Return to the top-level Git directory
alias gitroot="cd \$(git rev-parse --show-toplevel)"

# Compress the secrets folder to a .zip file
# Only works from the project root directory, use `gitroot` first
alias zipsecrets="zip -FSr secrets.zip secrets/"

# Clean up docker
alias dprune="docker system prune --volumes"

# Build the Sphinx documentation for all subprojects using Sphinx
build_sphinx () {
    pushd $(git rev-parse --show-toplevel)
    cd digital-hospitals-docs
    poetry run make clean  # IF not cleaned, new pages won't appear in TOC of existing pages
    poetry run make html

    # Add cd and make commands for each new subproject here
    popd
}

# Build the Sphinx documentation for all subprojects using Sphinx
dcdev () {
    pushd $(git rev-parse --show-toplevel)
    docker compose -f dockercompose-dev.yaml $@
    popd
}

# Refresh a running Docker Compose instance
dev_refresh() {
    build_sphinx
    dcdev build
    dcdev up -d
}