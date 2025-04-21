import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import tkinter as tk
from tkinter import messagebox

# Load your dataset
df = pd.read_csv("Book_Details.csv")  # Replace with your actual file path

# Encode categorical features
le_title = LabelEncoder()
le_author = LabelEncoder()

df['title_encoded'] = le_title.fit_transform(df['book_title'])
df['author_encoded'] = le_author.fit_transform(df['author'])

features = df[['title_encoded', 'author_encoded']]

# Fit NearestNeighbors model
model = NearestNeighbors(n_neighbors=6, metric='euclidean')
model.fit(features)

# Recommendation logic
def recommend_books(book_title, df, model):
    if book_title not in df['book_title'].values:
        return f"'{book_title}' not found in the dataset."
    
    idx = df[df['book_title'] == book_title].index[0]
    distances, indices = model.kneighbors([features.iloc[idx]])

    recommended_titles = df.iloc[indices[0]]['book_title'].tolist()
    return [title for title in recommended_titles if title != book_title]

# On search
def on_search(event=None):
    book_to_search = entry.get().strip()
    
    if not book_to_search:
        messagebox.showwarning("Input Error", "Please enter a book title.")
        return
    
    recommendations = recommend_books(book_to_search, df, model)
    
    listbox.delete(0, tk.END)
    
    if isinstance(recommendations, str):
        messagebox.showinfo("Not Found", recommendations)
    else:
        for i, title in enumerate(recommendations, 1):
            listbox.insert(tk.END, f"{i}. {title}")

# GUI setup
window = tk.Tk()
window.title("📚 Book Recommender")
window.geometry("550x450")
window.config(bg="#fdf6e3")  # Light cream background

# Fonts and Colors
font_label = ("Segoe UI", 12)
font_entry = ("Segoe UI", 11)
font_button = ("Segoe UI", 11, "bold")
font_listbox = ("Segoe UI", 10)

entry_bg = "#ffffff"
button_bg = "#007acc"
button_fg = "#ffffff"
listbox_bg = "#fff8dc"
listbox_fg = "#333333"

# Label
label = tk.Label(window, text="Enter a book title:", font=font_label, bg="#fdf6e3")
label.pack(pady=(20, 5))

# Entry
entry = tk.Entry(window, font=font_entry, width=40, bg=entry_bg, bd=2, relief="groove")
entry.pack(pady=(0, 10))
entry.bind("<Return>", on_search)

# Button
search_button = tk.Button(window, text="Get Recommendations", font=font_button,
                          bg=button_bg, fg=button_fg, activebackground="#005f99",
                          activeforeground="#ffffff", command=on_search, bd=0, padx=10, pady=5)
search_button.pack(pady=(0, 20))

# Listbox + Scrollbar
frame = tk.Frame(window, bg="#fdf6e3")
frame.pack()

scrollbar = tk.Scrollbar(frame, orient="vertical")
listbox = tk.Listbox(frame, font=font_listbox, width=50, height=10,
                     bg=listbox_bg, fg=listbox_fg, yscrollcommand=scrollbar.set,
                     bd=2, relief="sunken", selectbackground="#add8e6", highlightthickness=0)
scrollbar.config(command=listbox.yview)

listbox.pack(side="left", fill="y")
scrollbar.pack(side="right", fill="y")

# Focus cursor on entry
entry.focus()
window.mainloop()
