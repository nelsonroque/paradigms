library(readr)
library(dplyr)
library(ggplot2)

# read in chosen file
sweep.df <- read_csv(file.choose())

# calculate differences
sweep.df <- sweep.df %>% 
  mutate(radial_difference1 = line_angle_wrap360 - cue_angle1,
         radial_difference2 = line_angle_wrap360 - cue_angle2)

# recall decay by time since onset
ggplot(sweep.df,aes(n_updates,abs(radial_difference1))) + 
  geom_point(size=4) + 
  geom_smooth() +
  ggtitle("Recall decay by time since onset") +
  theme_bw()

# recall decay by time since onset
ggplot(sweep.df,aes(n_updates,abs(radial_difference2))) + 
  geom_point(size=4) + 
  geom_smooth() +
  ggtitle("Recall decay by time since onset") +
  theme_bw()

# recall decay by cue location
ggplot(sweep.df,aes(cue_angle1,radial_difference1)) + 
  geom_point(size=4) + 
  ggtitle("Recall decay by cue angle1") +
  geom_smooth() +
  #coord_polar()+
  theme_bw()

# recall decay by cue location
ggplot(sweep.df,aes(cue_angle1,radial_difference2)) + 
  geom_point(size=4) + 
  ggtitle("Recall decay by cue angle2") +
  geom_smooth() +
  #coord_polar()+
  theme_bw()


# recall decay by cue location
ggplot(sweep.df,aes(cue_angle2,radial_difference1)) + 
  geom_point(size=4) + 
  geom_smooth() +
  ggtitle("Recall decay by cue angle1") +
  #coord_polar()+
  theme_bw()

# recall decay by cue location
ggplot(sweep.df,aes(cue_angle2,radial_difference2)) + 
  geom_point(size=4) + 
  ggtitle("Recall decay by cue angle2") +
  geom_smooth() +
  #coord_polar()+
  theme_bw()
