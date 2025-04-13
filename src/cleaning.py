import pandas as pd

def clean_data(filepath):
    data = pd.read_csv(filepath)
    
    # Clean column names (strip spaces + lowercase)
    data.columns = data.columns.str.strip().str.lower()
    
    # Remove duplicates and handle missing data
    data = data.drop_duplicates()
    
    required_cols = ['patientid', 'medicinename', 'doctorname', 'date']
    data = data.dropna(subset=required_cols)
    
    text_cols = ['diagnosis', 'notes', 'dosage', 'frequency']
    data[text_cols] = data[text_cols].fillna('')
    
    data['price'] = pd.to_numeric(data['price'], errors='coerce').fillna(0.0)
    
    # Standardize doctor names (e.g., "dr. lisa ray" → "Dr. Lisa Ray")
    data['doctorname'] = data['doctorname'].str.title()
    
    # Fix dates (e.g., "not_a_date" becomes NaN and is dropped)
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data = data.dropna(subset=['date'])
    
    return data

# Load and clean data
cleaned_df = clean_data('digital-doctor-prescription/mocking_prescriptions_uncleaned.csv')

# Save cleaned data to CSV
cleaned_df.to_csv('cleaned_prescriptions.csv', index=False)