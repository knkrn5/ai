import pandas as pd
# import csv

# List of CSV file names with the required path format
csv_paths = [
    'wp-csv-data/wp-pages.csv', 
    'wp-csv-data/wp-home.csv', 
    'wp-csv-data/blog-categories.csv', 
    'wp-csv-data/fin-calculators.csv', 
    'wp-csv-data/fin-quizzes.csv', 
    'wp-csv-data/contact-info.csv', 
    'wp-csv-data/about-us.csv', 
    'wp-csv-data/our-team.csv', 
    'wp-csv-data/our-plan.csv'
]

# Load all CSV files into DataFrames
wp_pages_df = pd.read_csv(csv_paths[0])
wp_home_df = pd.read_csv(csv_paths[1])
blog_categories_df = pd.read_csv(csv_paths[2])
fin_calculators_df = pd.read_csv(csv_paths[3])
fin_quizzes_df = pd.read_csv(csv_paths[4])
contact_info_df = pd.read_csv(csv_paths[5])
about_us_df = pd.read_csv(csv_paths[6])
our_team_df = pd.read_csv(csv_paths[7])
our_plan_df = pd.read_csv(csv_paths[8])

# Check the first few rows of each DataFrame to verify the data
print(wp_pages_df.head())
print(wp_home_df.head())
print(blog_categories_df.head())
print(fin_calculators_df.head())
print(fin_quizzes_df.head())
print(contact_info_df.head())
print(about_us_df.head())
print(our_team_df.head())
print(our_plan_df.head())


