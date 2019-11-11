rm(list = ls())
#_________________________________________________________________________________________________________
usePackage <- function(p) {
    #Helper function to load/install packages
    if (!is.element(p, installed.packages()[,1]))
        install.packages(p, dep = TRUE)
    require(p, character.only = TRUE)
}
usePackage("tidyverse")
usePackage("rstudioapi")
WD = file.path(dirname(rstudioapi::getSourceEditorContext()$path)) 
setwd(WD)
####
####
csv_file_path = "../Raw CSV"
file_names = list.files(csv_file_path, full.names = TRUE)
#
col_names = names(read_csv(file_names[1]))
D = plyr::ldply(file_names, read_csv)
D = D[,which(names(D) %in% col_names)] %>%
    select(-X1)
write_csv(D,"../Aggregated Results.csv")
