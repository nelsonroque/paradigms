library(readr)
library(dplyr)
library(ggplot2)

# read in chosen file
zoom.df <- read_csv(file.choose())

# recall decay by time since onset
ggplot(zoom.df,aes(update_count,radial_difference)) + 
  geom_point(size=4) + 
  geom_smooth() +
  ggtitle("Recall decay by time since onset") +
  theme_bw()

# recall decay by cue size
ggplot(zoom.df,aes(cue_radius,radial_difference)) + 
  geom_point(size=4) + 
  geom_smooth() +
  ggtitle("Recall decay by cue size") +
  theme_bw()

zoom.df %>% 
  group_by(cue_radius) %>%
  summarise(m.diff = mean(radial_difference))