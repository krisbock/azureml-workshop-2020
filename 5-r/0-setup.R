# Install the azuremlsdk package
install.packages('remotes')

# Most likely will already be installed
remotes::install_cran('azuremlsdk', repos = 'https://cloud.r-project.org/')

# Install additional packages that will be used in this module
install.packages(c('data.table'))
