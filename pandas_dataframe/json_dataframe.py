import pandas as pd
# import json

# List of JSON file names with the required path format
json_paths = [
    'wp-json-data/about-us.json',
    'wp-json-data/blog-categories.json',
    'wp-json-data/contact-info.json',
    'wp-json-data/fin-calculators.json',
    'wp-json-data/fin-quizzes.json',
    'wp-json-data/our-plan.json',
    'wp-json-data/our-team.json',
    'wp-json-data/wp-home.json',
    'wp-json-data/wp-pages.json'
]

# Load all JSON files into DataFrames
about_us_df = pd.read_json(json_paths[0])  # For simple JSON structure
blog_categories_df = pd.read_json(json_paths[1])
contact_info_df = pd.read_json(json_paths[2])
fin_calculators_df = pd.read_json(json_paths[3])
fin_quizzes_df = pd.read_json(json_paths[4])
our_plan_df = pd.read_json(json_paths[5])
our_team_df = pd.read_json(json_paths[6])
wp_home_df = pd.read_json(json_paths[7])
wp_pages_df = pd.read_json(json_paths[8])

# Display the first few rows of each DataFrame to verify the data
print(about_us_df.head())
print(blog_categories_df.head())
print(contact_info_df.head())
print(fin_calculators_df.head())
print(fin_quizzes_df.head())
print(our_plan_df.head())
print(our_team_df.head())
print(wp_home_df.head())
print(wp_pages_df.head())
