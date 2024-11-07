import kagglehub
kagglehub.login()
# Download latest version
path = kagglehub.dataset_download("kanchana1990/uae-real-estate-2024-dataset")

print("Path to dataset files:", path)