import os
import pandas as pd
from docx import Document
import traceback

CERTIFICATE_FOLDER = "certificates"
LOG_FILE = os.path.join(CERTIFICATE_FOLDER, "sample.csv")

# Ensure folders and files
if not os.path.exists(CERTIFICATE_FOLDER):
    os.makedirs(CERTIFICATE_FOLDER)

if not os.path.exists(LOG_FILE):
    # Create the log file with default headers if it doesn't exist
    pd.DataFrame(columns=["Filename", "Downloads", "Prints"]).to_csv(LOG_FILE, index=False)

def extract_text_from_docx(filepath):
    doc = Document(filepath)
    return "<br>".join([p.text for p in doc.paragraphs])

def update_log(filename, action_type):
    try:
        print(f"[DEBUG] Logging action: {action_type} for {filename}")

        # Read the CSV file, creating a new one if it doesn't exist or is empty
        if os.path.getsize(LOG_FILE) == 0:  # Check if the file is empty
            print("[DEBUG] log.csv is empty. Creating new log entry.")
            df = pd.DataFrame(columns=["Filename", "Downloads", "Prints"])
        else:
            try:
                df = pd.read_csv(LOG_FILE, encoding="utf-8", encoding_errors="replace")
                print("[DEBUG] log.csv loaded successfully.")
            except pd.errors.ParserError as e:
                print(f"[ERROR] CSV parsing error: {e}")
                # Reinitialize the dataframe if the CSV is corrupted
                df = pd.DataFrame(columns=["Filename", "Downloads", "Prints"])
                print("[DEBUG] log.csv repaired (new empty DataFrame created).")

        # Add a new entry or update an existing one
        if filename not in df["Filename"].values:
            print(f"[DEBUG] Adding new entry for {filename}")
            new_entry = {
                "Filename": filename,
                "Downloads": 1 if action_type == "download" else 0,
                "Prints": 1 if action_type == "print" else 0,
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        else:
            print(f"[DEBUG] Updating existing entry for {filename}")
            index = df[df["Filename"] == filename].index[0]

            # Safely fill missing values
            if pd.isna(df.at[index, "Downloads"]):
                df.at[index, "Downloads"] = 0
            if pd.isna(df.at[index, "Prints"]):
                df.at[index, "Prints"] = 0

            if action_type == "download":
                df.at[index, "Downloads"] += 1
            elif action_type == "print":
                df.at[index, "Prints"] += 1

        # Save the updated DataFrame to CSV
        df.to_csv(LOG_FILE, index=False)
        print("[DEBUG] Log saved successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to update log: {e}")
        print(traceback.format_exc())  # print the full traceback
        raise e
