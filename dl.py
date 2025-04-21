import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tkinter as tk
from tkinter import messagebox

# Load the CSV data
file_path = r"C:\Users\DELL\Downloads\Book_Details.csv"
df = pd.read_csv(file_path)

# Clean the data
df_cleaned = df.drop(columns=['Unnamed: 0', 'book_id', 'cover_image_uri', 'book_title', 'authorlink'])
df_cleaned = df_cleaned.fillna(0)

# Convert categorical columns (e.g., genres) into numerical values using one-hot encoding
df_cleaned = pd.get_dummies(df_cleaned, columns=['genres', 'author'], drop_first=True)

# Ensure 'average_rating' is numeric
df_cleaned['average_rating'] = pd.to_numeric(df_cleaned['average_rating'], errors='coerce')

# Select the target column for training (e.g., we will predict 'average_rating' here)
X = df_cleaned.drop(columns=['average_rating'])  # Features
y = df_cleaned['average_rating']  # Target variable (average_rating)

# Scale the features (only numeric ones)
X_scaled = X.select_dtypes(include=[np.number])  # Select only numeric columns
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_scaled)

# Define the model
model = Sequential()
model.add(Dense(128, input_dim=X_scaled.shape[1], activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))  # Predicting a continuous value (e.g., average_rating)

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Train the model
model.fit(X_scaled, y, epochs=30, batch_size=32, verbose=1)

# Tkinter GUI for book recommendation
def on_recommend_click():
    book_name = entry.get()
    if book_name:
        # Find the closest match (based on average_rating for simplicity)
        # Filter books by name (You may want to match part of the name for better results)
        similar_books = df[df['book_title'].str.contains(book_name, case=False, na=False)]
        
        if not similar_books.empty:
            # If the user input matches any book title
            recommended_book = similar_books.iloc[0]
            recommendation = f"Recommended Book:\n{recommended_book['book_title']}\n" \
                             f"Author: {recommended_book['author']}\n" \
                             f"Rating: {recommended_book['average_rating']}\n"
        else:
            # If no exact match is found, suggest top-rated book
            top_rated_books = df.nlargest(1, 'average_rating')  # Top-rated book
            recommended_book = top_rated_books.iloc[0]
            recommendation = f"Could not find an exact match. Here's a highly rated book:\n" \
                             f"{recommended_book['book_title']}\n" \
                             f"Author: {recommended_book['author']}\n" \
                             f"Rating: {recommended_book['average_rating']}\n"
        
        # Show recommendation in a pop-up window
        messagebox.showinfo("Book Recommendation", recommendation)
    else:
        messagebox.showwarning("Input Error", "Please enter a book name.")

# Tkinter window setup
root = tk.Tk()
root.title("Book Recommender")
root.geometry("400x200")

# Input label and field
label = tk.Label(root, text="Enter Book Name:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Recommend button
recommend_button = tk.Button(root, text="Get Recommendation", command=on_recommend_click)
recommend_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
