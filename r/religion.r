library(pacman)
p_load(ggdist, here, tidyverse, stargazer)
source(here("r", "shaped_loaders.r"))
source(here("r", "plotting_functions.r"))

## Plots
### Correlations
df_religion_correlations <- load_religion_by_source(without_0 = TRUE, direction = "wide") %>%
  pivot_longer(cols = c("prop_muslim", "prop_christian"), names_to = "religion", values_to = "prop") %>%
  select(religion, prop, prop_positive, prop_negative, prop_porn, source) %>%
  mutate(religion = if_else(religion == "prop_muslim", "Muslim", "Christian"))

xlim_religion <- quantile(df_religion_correlations$prop, c(0.99))[[1]]
ylim_religion <- list()
n_within_quantile <- list()

for (variable in list("prop_positive", "prop_negative", "prop_porn")) {
  subset <- filter(df_religion_correlations, prop < xlim_religion)
  ylim_religion[[variable]] <- quantile(subset[[variable]], c(0.99))[[1]]

  n_within_quantile[[variable]] <- with(df_religion_correlations, sum(prop < ylim_religion[[variable]]))
}

scatter_with_correlation(
  data = df_religion_correlations,
  x = prop,
  y = prop_positive,
  fill = religion,
  color = religion,
  facet_rows = source,
  xlim = xlim_religion,
  ylim = ylim_religion$prop_positive,
  filename = "religion_positive_words_correlation",
  xlab = "Proportion of tokens that are the religion's pronoun",
  ylab = "Proportion of tokens that carry positive sentiment",
  point_alpha = 0.03,
  title = "Limited to 99th percentile on each axis.",
  colours = "brewer"
)

scatter_with_correlation(
  data = df_religion_correlations,
  x = prop,
  y = prop_negative,
  fill = religion,
  color = religion,
  facet_rows = source,
  xlim = xlim_religion,
  ylim = ylim_religion$prop_negative,
  filename = "religion_negative_words_correlation",
  xlab = "Proportion of tokens that are the religion's pronoun",
  ylab = "Proportion of tokens that are carry negative sentiment",
  point_alpha = 0.03,
  title = "Limited to 99th percentile on each axis."
)

scatter_with_correlation(
  data = df_religion_correlations,
  x = prop,
  y = prop_porn,
  fill = religion,
  color = religion,
  facet_rows = source,
  xlim = xlim_religion,
  ylim = ylim_religion$prop_porn,
  filename = "religion_porn_correlation",
  xlab = "Proportion of tokens that are the religion's pronoun",
  ylab = "Proportion of tokens that are porn",
  point_alpha = 0.09,
  title = "Limited to 99th percentile on each axis. \n Values are rounded to 0 if < 3 unique porn words in doc. \n Using wordlist from dfm, except ['kvinder', 'piger', 'damer', 'fanden']"
)

# LMs
lm_positive <- lm(prop_positive ~ (prop:religion) * source, data = df_religion_correlations)
lm_negative <- lm(prop_negative ~ (prop:religion) * source, data = df_religion_correlations)
lm_porn <- lm(prop_porn ~ (prop:religion) * source, data = df_religion_correlations)
stargazer(lm_positive, lm_negative, lm_porn, out = here("tables", "lm_religion.txt"))
stargazer(lm_positive, lm_negative, lm_porn, out = here("tables", "lm_religion.tex"))