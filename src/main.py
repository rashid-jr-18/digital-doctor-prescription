import cleaning

import uploadsql

# Step 1: Load and clean
df = cleaning.clean_data(r'digital-doctor-prescription\mocking_prescriptions_uncleaned.csv')



# Step 3: Upload to MySQL
uploadsql.upload_to_mysql(df, table_name='prescriptions')
