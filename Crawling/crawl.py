import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import mysql.connector
from tkinter import messagebox
import tkinter as tk

# Function to extract information from the Wikipedia page based on the disease name
def extract_info(disease_name):
    try:
        # Construct the URL based on the disease name
        url = "https://en.wikipedia.org/wiki/" + disease_name

        # Fetch the webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract disease name
        disease_name_tag = soup.find('span', {'class': 'mw-page-title-main'})
        if disease_name_tag:
            disease_name = disease_name_tag.text.strip()
        else:
            return "Error: Disease name not found."

        # Extract symptoms
        symptoms_tag = soup.find('a', {'title': 'Signs and symptoms'})
        if symptoms_tag:
            symptoms = symptoms_tag.find_next('td', {'class': 'infobox-data'}).text.strip()
        else:
            symptoms = "Symptoms not found."

        # Extract precautions
        precautions_tag = soup.find('th', text='Prevention')
        if precautions_tag:
            precautions = precautions_tag.find_next('td', {'class': 'infobox-data'}).text.strip()
        else:
            precautions = "Precautions not found."

        # Extract prevention methods
        prevention_tag = soup.find('span', {'id': 'Prevention'})
        if prevention_tag:
            prevention_text = prevention_tag.find_next('p').text.strip()
        else:
            prevention_text = "Prevention methods not found."

        # Extract antimalarial medication
        medication_tag = soup.find('a', {'title': 'Medication'})
        if medication_tag:
            medication = medication_tag.find_next('a', {'title': 'Antimalarial medication'}).text.strip()
        else:
            medication = "Antimalarial medication not found."

        # Translate data into Urdu
        translator = Translator()
        disease_name_urdu = translator.translate(disease_name, src='en', dest='ur').text
        symptoms_urdu = translator.translate(symptoms, src='en', dest='ur').text
        precautions_urdu = translator.translate(precautions, src='en', dest='ur').text
        prevention_text_urdu = translator.translate(prevention_text, src='en', dest='ur').text
        medication_urdu = translator.translate(medication, src='en', dest='ur').text

        return (disease_name_urdu, symptoms_urdu, precautions_urdu, prevention_text_urdu, medication_urdu)

    except Exception as e:
        return f"Error: {str(e)}"

# Function to handle search button click
def search():
    disease_name = entry_disease.get()
    if disease_name:
        # Extract information based on the entered disease name
        data = extract_info(disease_name)

        if data:
            # Display translated data to the user
            translated_info = "\n\n".join([f"{field.capitalize()}: {value}" for field, value in zip(["disease name", "symptoms", "precautions", "prevention methods", "medication"], data)])
            messagebox.showinfo("Translated Information", translated_info)

            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crawl_db"
            )
            cursor = connection.cursor()

            # Insert translated data into the database
            sql = "INSERT INTO diseases (disease_name, symptoms, precautions, prevention_methods, medication) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, data)
            connection.commit()

            messagebox.showinfo("Success", "Data has been translated and saved into the database.")
        else:
            messagebox.showerror("Error", "Failed to fetch data from Wikipedia.")
    else:
        messagebox.showwarning("Warning", "Please enter a disease name.")

# Create the GUI window
window = tk.Tk()
window.title("Wikipedia Disease Info")
window.geometry("400x200")

# Create a label and entry widget for entering the disease name
label_disease = tk.Label(window, text="Enter Disease Name:")
label_disease.pack(pady=5)
entry_disease = tk.Entry(window)
entry_disease.pack(pady=5)

# Create a search button
btn_search = tk.Button(window, text="Search", command=search)
btn_search.pack(pady=10)

# Run the GUI application
window.mainloop()
