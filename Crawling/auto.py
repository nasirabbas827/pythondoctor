import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import mysql.connector

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
        symptoms_tag = soup.find('span', {'id': 'Signs_and_symptoms'})
        if symptoms_tag:
            symptoms = symptoms_tag.find_next('p').text.strip()
        else:
            symptoms = "Symptoms not found."

        # Extract precautions
        precautions_tag = soup.find('span', {'id': 'Prevention'})
        if precautions_tag:
            precautions = precautions_tag.find_next('p').text.strip()
        else:
            precautions = "Precautions not found."

        # Extract prevention methods
        prevention_tag = soup.find('span', {'id': 'Prevention'})
        if prevention_tag:
            prevention_text = prevention_tag.find_next('p').text.strip()
        else:
            prevention_text = "Prevention methods not found."

        # Extract medication
        medication_tag = soup.find('span', {'id': 'Treatment'})
        if medication_tag:
            medication = medication_tag.find_next('p').text.strip()
        else:
            medication = "Medication not found."

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

# Function to auto search for diseases and save their information to the database
def auto_search_and_save():
    # List of diseases
    diseases = [
     "Naegleriasis", 
    "Necatoriasis", "Onchocerciasis","Achalasia", "Acromegaly", "Addison's disease", "Adenomyosis", "Alopecia areata", 
    "Amyloidosis", "Anemia", "Angioedema", "Ankylosing spondylitis", "Aortic aneurysm", 
    "Aplastic anemia", "Arteriosclerosis", "Asbestosis", "Asthma", "Atrial fibrillation", 
    "Barrett's esophagus", "Behcet's disease", "Benign prostatic hyperplasia", "Biliary cirrhosis", 
    "Blepharospasm", "Bronchiectasis", "Bullous pemphigoid", "Celiac disease", "Cervical dystonia", 
    "Charcot-Marie-Tooth disease", "Chronic granulomatous disease", "Chronic lymphocytic leukemia", 
    "Chronic myeloid leukemia", "Cluster headache", "Colitis", "Condyloma acuminatum", 
    "Congenital adrenal hyperplasia", "Congenital heart defect", "Conn's syndrome", 
    "Creutzfeldt-Jakob disease", "Crohn's disease", "Cushing's syndrome", "Cutaneous lupus erythematosus", 
    "Cystinuria", "Dandy-Walker syndrome", "Deep vein thrombosis", "Dermatitis herpetiformis", 
    "Dermatomyositis", "Diabetic neuropathy", "Diabetic retinopathy", "Diffuse large B-cell lymphoma", 
    "Dilated cardiomyopathy", "Diverticulitis", "Duchenne muscular dystrophy", "Dysautonomia", 
    "Dysphagia", "Eczema", "Ehlers-Danlos syndrome", "End-stage renal disease", "Epidermolysis bullosa", 
    "Epilepsy", "Erythromelalgia", "Essential tremor", "Exocrine pancreatic insufficiency", "Fabry disease", 
    "Familial adenomatous polyposis", "Familial hypercholesterolemia", "Fanconi anemia", "Felty's syndrome", 
    "Fibrodysplasia ossificans progressiva", "Focal segmental glomerulosclerosis", "Folliculitis", 
    "Friedreich's ataxia", "Frontotemporal dementia", "Gaucher disease", "Giant cell arteritis", 
    "Gilbert's syndrome", "Glaucoma", "Goodpasture's syndrome", "Granuloma annulare", "Graves' disease", 
    "Guillain-Barré syndrome", "Hashimoto's thyroiditis", "Hemochromatosis", "Henoch-Schönlein purpura","Abulia", "Acute stress disorder", "Adjustment disorder", "Agoraphobic avoidance", "Alexithymia", 
    "Amnesia", "Anhedonia"
    ]

    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crawl_db"
        )
        cursor = connection.cursor()

        for disease in diseases:
            # Extract information based on the disease name
            data = extract_info(disease)

            if data:
                # Insert translated data into the database
                sql = "INSERT INTO diseases (disease_name, symptoms, precautions, prevention_methods, medication) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, data)
                connection.commit()
                print(f"Successfully searched and saved information for {disease}.")

        cursor.close()
        connection.close()

        print("All diseases searched and saved successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Perform auto search and save
auto_search_and_save()
