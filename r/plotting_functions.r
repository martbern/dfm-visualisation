library("pacman")
source(here("r", "theme_publication.r"))

theme <- theme_Publication()

p_load(ggdist, gghalves, ggforce, devtools)
basic_rain <- function(data, x, y, fill, filename = FALSE, ylim = c(0, 0.05)) {
  plot <- ggplot(
    data,
    aes(
      x = {{ x }},
      y = {{ y }},
      fill = {{ fill }}
    )
  ) +
    geom_boxplot(
      width = .15,
      outlier.shape = NA
    ) +
    ggdist::stat_halfeye(
      ## custom bandwidth
      adjust = .5,
      ## adjust height
      width = .6,
      ## move geom to the right
      justification = -.2,
      ## remove slab interval
      .width = 0,
      point_colour = NA,
      alpha = 0.5
    ) +
    coord_flip() +
    scale_x_discrete() +
    ylim(ylim) +
    theme

  if (filename != FALSE) {
    ggsave(filename = paste0(filename, ".png"), width = 5, height = 5, path = here("plots"))
  }

  return(plot)
}

scatter_with_correlation <- function(data, x, y, fill, color, facet_rows, ylim, xlim, xlab, ylab = "", point_alpha, title = "", filename = FALSE, colours = c("#7300F7", "#18BA9A")) {
  plot <- ggplot(data, aes(x = {{ x }}, y = {{ y }}, fill = {{ fill }}, color = {{ color }})) +
    geom_point(, size = 1, alpha = {{ point_alpha }}) +
    geom_line(
      stat = "smooth", method = "lm",
      size = 0.5,
      alpha = 1
    ) +
    geom_smooth(method = "lm", se = TRUE, color = "black", alpha = 0.3, size = 0) +
    coord_cartesian(
      ylim = c(0, ylim),
      xlim = c(0, xlim)
    ) +
    facet_grid(rows = vars({{ facet_rows }})) +
    labs(title = {{ title }}, fill = "Gender", color = "Gender") +
    xlab({{ xlab }}) +
    ylab({{ ylab }})

  if (colours == "brewer") {
    plot <- plot +
      scale_colour_brewer(palette = "Set1", direction = -1) +
      scale_fill_brewer(palette = "Set1", direction = -1)
  } else {
    plot <- plot +
      scale_colour_manual(values = colours) +
      scale_fill_manual(values = colours)
  }

  if (filename != FALSE) {
    ggsave(filename = paste0(filename, ".png"), width = 10, height = 10, path = here("plots"))
  }

  return(plot)
}