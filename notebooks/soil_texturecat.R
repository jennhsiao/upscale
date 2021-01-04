### Classify soil texture
# coding this up in R since couldn't find good packages in Python

library('soiltexture')
library('dplyr')

df_soil <- read.csv('soiltexture_nass.csv')
df_soil <- rename(df_soil, SAND = sand)
df_soil <- rename(df_soil, SILT = silt)
df_soil <- rename(df_soil, CLAY = clay)
head(df_soil)


df_soilstocat <- data.frame(
  'CLAY' = c(df_soil['CLAY']),
  'SILT' = c(df_soil['SILT']),
  'SAND' = c(df_soil['SAND'])
)
head(df_soilstocat)


df_soiltext <-
  TT.points.in.classes(
    tri.data = df_soilstocat,
    class.sys = 'USDA.TT'
  )

head(df_soiltext)
