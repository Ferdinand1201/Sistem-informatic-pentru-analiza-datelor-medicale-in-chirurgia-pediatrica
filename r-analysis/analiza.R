# Încarcă biblioteca necesară
library(jsonlite)

# Încarcă datele exportate de FastAPI
df <- stream_in(file("../data/export_r.json"))


# Afișează datele
print(df)

# Exemplu simplu: medie HR și temperatură
cat("Media pulsului:", mean(df$heart_rate), "\n")
cat("Media temperaturii:", mean(df$temperature), "\n")
