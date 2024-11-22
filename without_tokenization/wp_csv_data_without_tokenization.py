import os
import pandas as pd
from datasets import Dataset, DatasetDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load all CSV files into DataFrames
wp_pages_df = pd.read_csv('data/wp-csv-data/wp-pages.csv')
wp_home_df = pd.read_csv('data/wp-csv-data/wp-home.csv')
blog_categories_df = pd.read_csv('data/wp-csv-data/blog-categories.csv')
fin_calculators_df = pd.read_csv('data/wp-csv-data/fin-calculators.csv')
fin_quizzes_df = pd.read_csv('data/wp-csv-data/fin-quizzes.csv')
contact_info_df = pd.read_csv('data/wp-csv-data/contact-info.csv')
about_us_df = pd.read_csv('data/wp-csv-data/about-us.csv')
our_team_df = pd.read_csv('data/wp-csv-data/our-team.csv')
our_plan_df = pd.read_csv('data/wp-csv-data/our-plan.csv')

# Function to standardize DataFrame structure
def standardize_dataframe(df, required_columns=['wp nav', 'wp nav_link']):
    # Create missing columns with empty strings if they don't exist
    for col in required_columns:
        if col not in df.columns:
            df[col] = ''
    
    # Ensure only required columns are present and in the correct order
    return df[required_columns]

# Dictionary mapping original column names to standardized names
column_mappings = {
    'modules': 'wp nav',
    'modules content': 'wp nav_link',
    'blog categories': 'wp nav',
    # Add more mappings as needed for other dataframes
}

# Rename and standardize all dataframes
dataframes = {
    'wp_pages': wp_pages_df,
    'wp_home': wp_home_df.rename(columns=column_mappings),
    'blog_categories': blog_categories_df,
    'fin_calculators': fin_calculators_df,
    'fin_quizzes': fin_quizzes_df,
    'contact_info': contact_info_df,
    'about_us': about_us_df,
    'our_team': our_team_df,
    'our_plan': our_plan_df
}

# Standardize all dataframes
standardized_dataframes = {
    name: standardize_dataframe(df) 
    for name, df in dataframes.items()
}

# Create a Hugging Face DatasetDict with standardized features
non_tokenized_data = DatasetDict({
    name: Dataset.from_pandas(df)
    for name, df in standardized_dataframes.items()
})

# Print dataset info for verification
print("Dataset structure:")
print(non_tokenized_data)
print("\nSample data from wp_pages:")
print(standardized_dataframes['wp_pages'].head())

# Push the dataset to the Hugging Face Hub
DATASET_NAME = "wealthpsychology-raw-data"
DESCRIPTION = "This dataset contains raw data for the Wealth Psychology website content."

""" non_tokenized_data.push_to_hub(
    repo_id=DATASET_NAME,
    private=False,
    token=os.getenv("HUGGING_FACE_WRITE_API")
) """