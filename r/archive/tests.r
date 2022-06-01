library("pacman")

p_load(testthat, here, datapasta)

source(here("functions.r"))
       
test_that("Column value is correct", {
  test_df <- tribble(
    ~col1, ~col2, ~col3, ~col4,
    1, 2, 3, 4,
  )
  
  output_df <- sum_every_n_rows(test_df, 4)
  
  expect_equal(
    output_df[["col1"]],
    10,
    tolerance = 1e-4)
})


