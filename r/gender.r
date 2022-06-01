library(pacman)
p_load(ggdist, here, tidyverse, stargazer)
source(here("r", "shaped_loaders.r"))
source(here("r", "plotting_functions.r"))

## Plots
### Correlations
df_pronoun_correlations <- load_gender_pronoun_by_source(without_0 = TRUE, direction = "wide") %>%
  pivot_longer(cols = c("prop_pronoun_male", "prop_pronoun_female"), names_to = "gender", values_to = "prop") %>%
  select(gender, prop, prop_positive, prop_negative, prop_porn, source) %>%
  mutate(gender = if_else(gender == "prop_pronoun_male", "Male", "Female"))

xlim <- quantile(df_pronoun_correlations$prop, c(0.99))[[1]]
ylim <- list()
n_within_quantile <- list()

for (variable in list("prop_positive", "prop_negative", "prop_porn")) {
  subset <- filter(df_pronoun_correlations, prop < xlim)
  ylim[[variable]] <- quantile(subset[[variable]], c(0.99))[[1]]

  n_within_quantile[[variable]] <- with(df_pronoun_correlations, sum(prop < ylim[[variable]]))
}

scatter_with_correlation(
  data = df_pronoun_correlations,
  x = prop,
  y = prop_positive,
  fill = gender,
  color = gender,
  facet_rows = source,
  xlim = xlim,
  ylim = ylim$prop_positive,
  filename = "pronoun_positive_words_correlation",
  xlab = "Proportion of tokens that are the gender's pronoun",
  ylab = "Proportion of tokens that carry positive sentiment",
  point_alpha = 0.03,
  title = "Limited to 99th percentile on each axis."
)

scatter_with_correlation(
  data = df_pronoun_correlations,
  x = prop,
  y = prop_negative,
  fill = gender,
  color = gender,
  facet_rows = source,
  xlim = xlim,
  ylim = ylim$prop_negative,
  filename = "pronoun_negative_words_correlation",
  xlab = "Proportion of tokens that are the gender's pronoun",
  ylab = "Proportion of tokens that are carry negative sentiment",
  point_alpha = 0.03,
  title = "Limited to 99th percentile on each axis."
)

scatter_with_correlation(
  data = df_pronoun_correlations,
  x = prop,
  y = prop_porn,
  fill = gender,
  color = gender,
  facet_rows = source,
  xlim = xlim,
  ylim = ylim$prop_porn,
  filename = "pronoun_porn_correlation",
  xlab = "Proportion of tokens that are the gender's pronoun",
  ylab = "Proportion of tokens that are porn",
  point_alpha = 0.09,
  title = "Limited to 99th percentile on each axis. \n Values are rounded to 0 if < 3 unique porn words in doc. \n Using wordlist from dfm, except ['kvinder', 'piger', 'damer', 'fanden']"
)

# LMs
lm_positive <- lm(prop_positive ~ (prop:gender) * source, data = df_pronoun_correlations)
lm_negative <- lm(prop_negative ~ (prop:gender) * source, data = df_pronoun_correlations)
lm_porn <- lm(prop_porn ~ (prop:gender) * source, data = df_pronoun_correlations)
stargazer(lm_positive, lm_negative, lm_porn, out = here("tables", "lm_gender.txt"))
stargazer(lm_positive, lm_negative, lm_porn, out = here("tables", "lm_gender.tex"))