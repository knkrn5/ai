from huggingface_hub import login
from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()


# Login to Hugging Face (you will be prompted for your Hugging Face token)
login(token=user_secrets.get_secret("hugging_face_write"))

from huggingface_hub import upload_folder

# Path to the folder containing your trained model
folder_path = "./final_model"  # the location of your final model

# Your Hugging Face model repository name (ensure the repository exists)
repo_name = "knkrn5/wealthpsychology_fine_tuned_with_gpt2"  # Replace with your Hugging Face model name

# Upload the folder to Hugging Face and overwrite the existing files
upload_folder(
    folder_path=folder_path,  # Path to your trained model files
    repo_id=repo_name,  # Repository name on Hugging Face
    path_in_repo=".",  # Place all files in the root of the repository
    #overwrite=True  # Overwrite existing files in the repository
)