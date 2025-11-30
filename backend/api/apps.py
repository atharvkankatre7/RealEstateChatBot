from django.apps import AppConfig
import pandas as pd
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    # Global variable to store the DataFrame
    real_estate_df = None
    
    def ready(self):
        """Load Excel file on startup"""
        if ApiConfig.real_estate_df is None:
            try:
                # Get the path to the Excel file
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                excel_path = os.path.join(base_dir, 'data', 'realestate.xlsx')
                
                # Load the Excel file
                ApiConfig.real_estate_df = pd.read_excel(excel_path)
                
                # Clean column names (strip whitespace)
                ApiConfig.real_estate_df.columns = ApiConfig.real_estate_df.columns.str.strip()
                
                print(f"✅ Successfully loaded real estate data with {len(ApiConfig.real_estate_df)} rows")
                print(f"📊 Localities: {ApiConfig.real_estate_df['final location'].unique().tolist()}")
            except Exception as e:
                print(f"❌ Error loading Excel file: {e}")
                # Create empty DataFrame if loading fails
                ApiConfig.real_estate_df = pd.DataFrame()
