library(pacman)
pacman::p_load(tidyverse, shiny,tsne, ggbiplot, GGally, stream, streamMOA)


pap = read_csv("C:/Users/henke/Documents/results.csv")

cat = unique(pap$category)

sel = pap %>%
  filter(category==cat[1])%>%
  filter(phrase=="simulate")
