import pandas as pd

# File paths
main_dataset_path = 'C:/Users/admin/Desktop/projects/the micro modern project/Data set/main_data_set.xlsx'
javan_dataset_path = 'C:/Users/admin/Desktop/projects/the micro modern project/Data set/daily scraping/time_series_data_javan.xlsx'
sisoog_dataset_path = 'C:/Users/admin/Desktop/projects/the micro modern project/Data set/daily scraping/time_series_data_sisoog.xlsx'

# Step 1: Load the existing main dataset (if it exists), otherwise create an empty DataFrame
try:
    main_df = pd.read_excel(main_dataset_path)
    print(f"Main dataset loaded from {main_dataset_path}")
except FileNotFoundError:
    main_df = pd.DataFrame()  # If the file doesn't exist, create an empty DataFrame
    print("Main dataset does not exist, creating a new one.")

# Step 2: Load the new datasets (javan and sisoog)
javan_df = pd.read_excel(javan_dataset_path)
print(f"Javan dataset loaded from {javan_dataset_path}")

sisoog_df = pd.read_excel(sisoog_dataset_path)
print(f"Sisoog dataset loaded from {sisoog_dataset_path}")

# Step 3: Concatenate the new datasets with the main dataset
# We use `ignore_index=True` to reset the index after concatenation
updated_df = pd.concat([main_df, javan_df, sisoog_df], ignore_index=True)

updated_df = updated_df.drop_duplicates(subset=['part_name', 'date'], keep='last')

# Step 4: Save the updated dataset back to the main file
updated_df.to_excel(main_dataset_path, index=False)
print(f"Updated main dataset saved to {main_dataset_path}")
