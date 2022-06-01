library(pacman)
p_load(ggdist, here, tidyverse, skimr)
source(here("r", "shaped_loaders.r"))
source(here("r", "plotting_functions.r"))
source(here("r", "theme_publication.r"))

unshaped_path <- here("data", "unshaped")

dfm <- read_csv(here("data", "shaped", "dfm.csv"))

dfm_sampled <- dfm %>%
    slice_sample(prop = 0.001)

xlim <- quantile(dfm$tokens, 0.99, na.rm = TRUE)

tokens_by_source <- ggplot(dfm, aes(x = tokens, fill = source)) +
    theme_Publication() +
    geom_histogram(binwidth = 10) +
    facet_grid(rows = vars(source), scales = "free") +
    coord_cartesian(xlim = c(0, xlim)) +
    labs(title = "x-axis is limited to 99th percentile.", x = "Tokens", y = "Document count") +
    theme(legend.position = "none") +
    scale_colour_brewer(palette = "Set1", direction = -1) +
    scale_fill_brewer(palette = "Set1", direction = -1)

ggsave(file = here("plots", "document_length_by_source.png"), width = 12, height = 12, dpi = 150)

filtered <- dfm %>%
    filter(tokens > 50000) %>%
    group_by(source) %>%
    summarise(n = n())

skim(grouped$tokens)