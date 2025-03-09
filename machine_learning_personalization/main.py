import pandas as pd
import logging
from src.data_collection import collect_user_behavior, save_data_to_csv
from src.data_processing import load_data, clean_data, save_cleaned_data
from src.database import Database
from src.recommendation_system import RecommendationSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Step 1: Collect user behavior data
    logging.info("Collecting user behavior data...")
    user_data = []
    num_users = 3  # Number of users to simulate
    num_entries_per_user = 10  # Number of entries per user

    for user_id in range(1, num_users + 1):
        user_data.extend(collect_user_behavior(user_id=user_id, num_entries=num_entries_per_user))
    
    save_data_to_csv(user_data)
    
    # Step 2: Load and clean the data
    logging.info("Loading and cleaning data...")
    df = load_data()
    cleaned_df = clean_data(df)
    save_cleaned_data(cleaned_df)

    # Step 3: Store cleaned data in the database
    logging.info("Storing cleaned data in the database...")
    db = Database()
    db.insert_data(cleaned_df.values.tolist())  # Convert DataFrame to list of tuples
    db.close_connection()

    # Step 4: Train the recommendation model
    logging.info("Training the recommendation model...")
    recommender = RecommendationSystem()
    recommender.train(cleaned_df)
    recommender.save_model()

    # Step 5: Example of making recommendations
    new_user_data = pd.DataFrame({
        'temperature': [22.0],
        'humidity': [60.0]
    })
    recommendations = recommender.recommend(new_user_data)
    logging.info(f"Recommendations for new user data: {recommendations}")

if __name__ == "__main__":
    main()
