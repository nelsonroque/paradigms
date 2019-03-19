library(readr)
library(dplyr)
library(ggplot2)

# read in chosen file
LR.df <- read_csv(file.choose())

LR.df <- LR.df %>%
  mutate(side = substr(cue,1,1))

# recall decay by time since onset
ggplot(LR.df,aes(trial,RT,color=SIDE)) + 
  geom_point(size=4) + 
  geom_smooth() +
  ggtitle("Recall decay by time since onset") +
  theme_bw()

LR.df %>% group_by(cue) %>%
  summarise(m.RT = mean(RT),
            ACC = mean(ACC))

LR.df %>% group_by(side) %>%
   summarise(m.RT = mean(RT),
            ACC = mean(ACC))

LR.df %>% group_by(case_shown) %>%
  summarise(m.RT = mean(RT),
            ACC = mean(ACC))
