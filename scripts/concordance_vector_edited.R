# From https://github.com/roblanf/concordance_vectors/blob/main/concordance_vector.R
# Changed to drop site concordance factors, on 17OCT24, by Jonas Lescroart

library(tidyverse)

# Read the data files
gcf <- read_table("gcf.cf.stat", comment = "#")

# Process the gcf file
gcv <- gcf %>%
  rename(gene_psi1 = gCF, 
         gene_psi1_N = gCF_N, 
         gene_N = gN,
         gene_psi4 = gDFP,
         gene_psi4_N = gDFP_N) %>%
  rowwise() %>%
  mutate(gene_psi2 = max(gDF1, gDF2),
         gene_psi3 = min(gDF1, gDF2),
         gene_psi2_N = max(gDF1_N, gDF2_N),
         gene_psi3_N = min(gDF1_N, gDF2_N)) %>%
  ungroup() %>%
  select(ID, gene_psi1, gene_psi2, gene_psi3, gene_psi4, gene_psi1_N, gene_psi2_N, gene_psi3_N, gene_psi4_N, gene_N)


# Write to CSV
write_csv(gcv, "concordance_vectors.csv")
