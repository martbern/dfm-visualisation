library("pacman")
p_load(here, tidyverse)

load_shaped_csv <- function(filename_prefix, without_0, direction) {
    if (without_0 == TRUE) {
        without_0 <- "_without_0"
    } else {
        without_0 <- ""
    }

    filename <- paste0(filename_prefix, direction, without_0, ".csv")

    file_path <- here("data", "shaped", filename)
    return(read_csv(file_path))
}

load_gender_pronoun_by_source <- function(without_0, direction) {
    return(load_shaped_csv(
        filename_prefix = "pronoun_by_source_",
        without_0 = without_0,
        direction = direction
    ))
}

load_religion_by_source <- function(without_0, direction) {
    return(load_shaped_csv(
        filename_prefix = "religion_by_source_",
        without_0 = without_0,
        direction = direction
    ))
}