import streamlit as st
import sqlite3
import bcrypt
import io
import cv2
import face_recognition
import time

# Connexion à la base de données SQLite
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    photo BLOB
)''')
conn.commit()

# Hashage du mot de passe
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode(), hashed_password.encode())

# Convertir une image en BLOB pour stockage
def convert_image_to_blob(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# Sauvegarder un utilisateur dans la base de données
def save_user(name, email, password, photo):
    hashed_pw = hash_password(password)
    cursor.execute("INSERT INTO users (name, email, password, photo) VALUES (?, ?, ?, ?)", 
                   (name, email, hashed_pw, photo))
    conn.commit()

# Récupérer un utilisateur par email
def get_user(email):
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cursor.fetchone()

def facial_recognition_live():
    st.write(" **Veuillez regarder la caméra pour la reconnaissance faciale**")

    # Charger les visages de la base de données
    cursor.execute("SELECT name, photo, email FROM users")
    users = cursor.fetchall()
    
    known_faces = []
    known_names = []
    known_emails = []

    for name, stored_photo, email in users:
        stored_image = face_recognition.load_image_file(io.BytesIO(stored_photo))
        stored_encoding = face_recognition.face_encodings(stored_image)

        if stored_encoding:  # Vérifier si un visage est détecté
            known_faces.append(stored_encoding[0])
            known_names.append(name)
            known_emails.append(email)


    if not known_faces:
        st.error("Aucune donnée de visage trouvée en base de données.")
        return

    # Ouvrir la webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Impossible d'accéder à la caméra.")
        return

    frame_placeholder = st.empty()  # Zone pour afficher la vidéo
    start_time = time.time()

    while time.time() - start_time < 10:  # Capture pendant 10 secondes
        ret, frame = cap.read()
        if not ret:
            st.error("Erreur lors de la capture vidéo.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        recognized_name = "Inconnu"

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)
            if True in matches:
                match_index = matches.index(True)
                recognized_name = known_names[match_index]
                recognized_email = known_emails[match_index]
                st.success(f"Bienvenue {recognized_name} !")

                # Mise à jour de l'état de connexion
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = recognized_email  # Utiliser le nom de l'utilisateur pour l'authentification
                st.session_state["user_info"] = {"name": recognized_name, "email": recognized_email}
                

                # Redirection vers la page d'accueil après la reconnaissance
                st.switch_page("pages/home.py")
                cap.release()
                cv2.destroyAllWindows()
                return  # Arrêter la boucle après reconnaissance

        # Affichage en direct dans Streamlit
        frame_placeholder.image(frame, channels="BGR")

    cap.release()
    cv2.destroyAllWindows()
    st.error("Visage non reconnu.")


