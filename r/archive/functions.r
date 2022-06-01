sum_every_n_rows <- function(df, batch_size) {
  new_df <- data.frame(matrix(NA, nrow = nrow(df), ncol = 1))

  for (i in 0:(ncol(df) / batch_size - 1)) {
    start_col_index <- 1 + batch_size * i

    colname <- colnames(df)[start_col_index]

    sum_slice <- c((start_col_index):(start_col_index + batch_size - 1))

    new_col <- df %>%
      rowwise() %>%
      mutate({{ colname }} := sum(c_across(sum_slice))) %>%
      select({{ colname }})

    new_df <- bind_cols(new_df, new_col)
  }

  return(new_df)
}

add_token_prop <- function(data, col) {
  mutate(data, "{{col}}_token_prop" := {{ col }} / tokens)
}