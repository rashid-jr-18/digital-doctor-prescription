import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class PrescriptionAnalyzer:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Root@123',
            database='doctors_prescription'
        )
        
    def fetch_data(self, query):
        return pd.read_sql(query, self.connection)

    def show_menu(self):
        while True:
            print("\n===== Digital Doctor Prescription Analysis =====")
            print("1. Most Common Diagnoses")
            print("2. Monthly Diagnosis Trends")
            print("3. Most Prescribed Medicines")
            print("4. New Emerging Diagnoses")
            print("5. Doctor Specific Prescription")
            print("6. Revenue by Diagnosis")
            print("7. Medicine Price Distribution")
            print("8. Doctor-Specific Revenue")
            print("9. Exit")
            
            choice = input("\nEnter your choice (1-9): ")
            
            if choice == '1':
                self.show_common_diagnoses()
            elif choice == '2':
                self.show_monthly_trends()
            elif choice == '3':
                self.show_top_medicines()
            elif choice == '4':
                self.show_emerging_diagnoses()
            elif choice == '5':
                self.show_doctor_patterns()
            elif choice == '6':
                self.show_revenue_diagnosis()
            elif choice == '7':
                self.show_price_distribution()
            elif choice == '8':
                self.show_doctor_revenue()
            elif choice == '9':
                print("\nExiting program...")
                break
            else:
                print("\nInvalid choice! Please try again.")
                
            input("\nPress Enter to return to menu...")

    def show_common_diagnoses(self):
        query = """
            SELECT diagnosis, COUNT(*) as count 
            FROM prescriptions 
            GROUP BY diagnosis 
            ORDER BY count DESC 
            LIMIT 10
        """
        df = self.fetch_data(query)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='count', y='diagnosis', data=df, palette='Blues_d')
        plt.title('Top 10 Most Common Diagnoses')
        plt.xlabel('Number of Cases')
        plt.tight_layout()
        plt.show()

    def show_monthly_trends(self):
        query = """
            SELECT DATE_FORMAT(date, '%Y-%m') as month, 
                   diagnosis, 
                   COUNT(*) as cases
            FROM prescriptions 
            GROUP BY month, diagnosis
        """
        df = self.fetch_data(query)
        
        # Get top 5 diagnoses
        top_diagnoses = df.groupby('diagnosis')['cases'].sum().nlargest(5).index.tolist()
        
        # Filter and pivot data
        df_top = df[df['diagnosis'].isin(top_diagnoses)]
        pivot_df = df_top.pivot(index='month', columns='diagnosis', values='cases').fillna(0)
        
        # Sort months chronologically
        pivot_df = pivot_df.sort_index()
        
        # Create plot
        plt.figure(figsize=(14, 8))
        
        # Set bar positions
        months = pivot_df.index
        x = np.arange(len(months))
        bar_width = 0.15
        
        # Create bars for each diagnosis
        for i, diagnosis in enumerate(top_diagnoses):
            plt.bar(
                x + (i * bar_width), 
                pivot_df[diagnosis], 
                width=bar_width, 
                label=diagnosis,
                color=plt.cm.tab10(i)
            )
        
        # Formatting
        plt.title('Monthly Cases of Top 5 Diagnoses', fontweight='bold', pad=20)
        plt.xlabel('Month', fontweight='bold')
        plt.ylabel('Number of Cases', fontweight='bold')
        plt.xticks(x + bar_width*2, months, rotation=45, ha='right')
        plt.legend(title='Diagnosis', bbox_to_anchor=(1.05, 1))
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, month in enumerate(months):
            for j, diagnosis in enumerate(top_diagnoses):
                value = pivot_df.loc[month, diagnosis]
                if value > 0:
                    plt.text(
                        x[i] + (j * bar_width) - 0.05,
                        value + 0.5,
                        f'{int(value)}',
                        fontsize=8,
                        color='black'
                    )
        
        plt.tight_layout()
        plt.show()

    def show_top_medicines(self):
        query = """
            SELECT medicinename, COUNT(*) as count 
            FROM prescriptions 
            GROUP BY medicinename 
            ORDER BY count DESC 
            LIMIT 10
        """
        df = self.fetch_data(query)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='count', y='medicinename', data=df, palette='Greens_d')
        plt.title('Top 10 Most Prescribed Medicines')
        plt.xlabel('Prescription Count')
        plt.tight_layout()
        plt.show()

    def show_emerging_diagnoses(self):
        query = """
            SELECT DATE_FORMAT(date, '%Y-%m') as month, 
                   COUNT(DISTINCT diagnosis) as new_diseases
            FROM prescriptions
            GROUP BY month
            ORDER BY month
        """
        df = self.fetch_data(query)
        
        plt.figure(figsize=(12, 6))
        plt.bar(df['month'], df['new_diseases'], color='salmon')
        plt.title('New Diseases Found Each Month\n(Higher bars = More new diseases discovered)')
        plt.ylabel('New Diseases Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_doctor_patterns(self):
        query = """
            SELECT 
                TRIM(LOWER(doctorname)) as clean_name,
                COUNT(*) as total_prescriptions
            FROM prescriptions 
            GROUP BY clean_name
            ORDER BY total_prescriptions DESC 
            LIMIT 5
        """
        df = self.fetch_data(query)
        
        # Clean names for display
        df['doctorname'] = df['clean_name'].str.title()
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(df['doctorname'], df['total_prescriptions'], color='orange')
        plt.title('Top 5 Busiest Doctors\n(Total Prescriptions)')
        plt.xlabel('Number of Prescriptions')
        
        # Add numbers
        for bar in bars:
            width = bar.get_width()
            plt.text(width+2, bar.get_y()+0.3, f'{int(width)}', ha='left')
        
        plt.tight_layout()
        plt.show()

    def show_revenue_diagnosis(self):
        query = """
            SELECT diagnosis, SUM(price) as total_revenue 
            FROM prescriptions 
            GROUP BY diagnosis 
            ORDER BY total_revenue DESC 
            LIMIT 10
        """
        df = self.fetch_data(query)
        plt.figure(figsize=(12, 6))
        sns.barplot(x='total_revenue', y='diagnosis', data=df, palette='Reds_d')
        plt.title('Top 10 Revenue Generating Diagnoses')
        plt.xlabel('Total Revenue')
        plt.tight_layout()
        plt.show()

    def show_price_distribution(self):
        query = "SELECT price FROM prescriptions WHERE price > 0"
        df = self.fetch_data(query)
        
        plt.figure(figsize=(12, 6))
        sns.histplot(df['price'], bins=10, color='skyblue', edgecolor='black')
        plt.title('Common Medicine Prices\n(Where most prices fall)')
        plt.xlabel('Price (₹)')
        
        # Add average line
        avg_price = df['price'].mean()
        plt.axvline(avg_price, color='red', linestyle='--')
        plt.text(avg_price*1.1, plt.ylim()[1]*0.9, 
                 f"Average Price: ₹{avg_price:.2f}", color='red')
        
        plt.tight_layout()
        plt.show()

    def show_doctor_revenue(self):
        query="""SELECT 
            TRIM(LOWER(doctorname)) as clean_name,
            SUM(price) as total_revenue 
        FROM prescriptions 
        GROUP BY clean_name
        ORDER BY total_revenue DESC 
        LIMIT 5
        """
        df = self.fetch_data(query)
    
    # Clean names for display
        df['doctorname'] = df['clean_name'].str.title()
    
        plt.figure(figsize=(10, 5))
        sns.barplot(x='total_revenue', 
                y='doctorname', 
                data=df, 
                palette='mako',
                order=df.sort_values('total_revenue', ascending=False)['doctorname'])
        plt.title('Top 5 Doctors by Revenue', fontweight='bold')
        plt.xlabel('Total Revenue (₹)', fontsize=12)
        plt.ylabel('Doctor Name', fontsize=12)
    
    # Add value labels
        for index, value in enumerate(df['total_revenue']):
            plt.text(value, index, f'₹{value:,.2f}', va='center')
    
        plt.tight_layout()
      
    
    
    
    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()
            

if __name__ == "__main__":
    analyzer = PrescriptionAnalyzer()
    analyzer.show_menu()