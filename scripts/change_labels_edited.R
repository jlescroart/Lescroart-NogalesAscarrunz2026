# From https://github.com/roblanf/concordance_vectors/blob/main/change_labels.R
# Changed to display all four gene concordance factors 
# instead of first gene, first site and first quartet concordance factor
# on 17OCT24, by Jonas Lescroart

# Load necessary libraries
library(ape)
library(tidyverse)

# Read the tree file
treeo <- read.tree("gcf.cf.branch")
tree <- treeo

# Read the CSV file
concordance_data <- read_csv("concordance_vectors.csv")

# Prepare the label information
concordance_data <- concordance_data %>%
    mutate(new_label = paste0(ID, ":g1_", gene_psi1, ",g2_", gene_psi2, ",g3_", gene_psi3, ",g4_", gene_psi4))

# Create a lookup table for the new labels
label_lookup <- setNames(concordance_data$new_label, as.character(concordance_data$ID))

# Assign new labels to node labels
tree$node.label <- sapply(tree$node.label, function(x) {
    new_label <- label_lookup[as.character(x)]
    if(is.na(new_label)) return(x) else return(new_label)
})

# fix the names
names(tree$node.label) = treeo$node.label

write.nexus(tree, file = "id_gcf_vector.nex")

