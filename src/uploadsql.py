
import mysql.connector

# In uploadsql.py
def upload_to_mysql(df, table_name):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Root@123',
        database='doctors_prescription'
    )
    cursor = conn.cursor()

    try:
        for index, row in df.iterrows():
            sql = """
            INSERT INTO prescriptions 
                (PatientID, DoctorName, MedicineName, Dosage, Frequency, Date, Diagnosis, Notes, Price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (
                row['patientid'], 
                row['doctorname'], 
                row['medicinename'],
                row['dosage'], 
                row['frequency'], 
                row['date'], 
                row['diagnosis'], 
                row['notes'], 
                row['price']
            )
            try:
                cursor.execute(sql, val)
            except mysql.connector.Error as err:
                print(f"Error inserting row {index}: {err}")
                print(f"Problematic data: {val}")
                # Optionally: continue or break
        conn.commit()
    finally:
        conn.close()
    
    print("Data inserted successfully.")