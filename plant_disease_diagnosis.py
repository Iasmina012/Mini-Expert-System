import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import backend
from backend import process_symptoms

# Functia pentru trimiterea simptomelor catre backend si obtinerea rezultatelor
def submit_symptoms():
    for i, entry in enumerate(symptom_entries):
        symptom = entry.get()
        if symptom:
            results = process_symptoms([symptom])
            if results:
                result_labels[i].config(text="\n".join(results))
                disease_index = list(backend.database.values()).index(results[0].split(" -> ")[1])
                if disease_index != -1:
                    # Afiseaza imaginea corespunzatoare bolii
                    disease_name = results[0].split(" -> ")[1]
                    image_path = backend.disease_images.get(disease_name)
                    if image_path:
                        image = Image.open(image_path)
                        image = image.resize((200, 100))
                        photo = ImageTk.PhotoImage(image)
                        image_label = tk.Label(root, image=photo)
                        image_label.image = photo
                        image_label.place(relx=0.75, rely=0.3+0.15*(i-1))
                        image_labels.append(image_label)
                        # Legam imaginea de functia care o va mari
                        image_label.bind("<Button-1>", lambda event, path=image_path: enlarge_image(path))
            else:
                result_labels[i].config(text="Nu s-au gasit boli asociate acestui simptom.")
        else:
            result_labels[i].config(text="")

# Functia pentru stergerea campurilor de introducere si a rezultatelor
def clear_all():

    # Simptome
    for entry in symptom_entries:
        entry.delete(0, tk.END)
    # Boli

    for label in result_labels:
        label.config(text="")
    # Imagini

    for image_label in image_labels:
        image_label.destroy()
    image_labels.clear()

# Functia pentru schimbarea culorii butonului pentru hover
def on_enter_button(event):
    event.widget.config(bg="#a2cffe")

# Functia pentru revenirea la culoarea originala a butonului
def on_leave_button(event):
    event.widget.config(bg="#63ace5")

# Functia pentru schimbarea culorii de fundal la hover pentru labels
def on_enter_label(event):
    event.widget.config(bg="#aed9e0", fg="black")

# Functia pentru revenirea la culoarea originala pentru labels
def on_leave_label(event):
    event.widget.config(bg="#63ace5", fg="white")

# Functia pentru extinderea intr-o noua fereastra a imaginii
def enlarge_image(image_path):
    enlarge_window = tk.Toplevel(root)
    enlarge_window.title("PlantMed - Imaginea Bolii")
    enlarged_image = Image.open(image_path)
    photo = ImageTk.PhotoImage(enlarged_image)
    label = tk.Label(enlarge_window, image=photo)
    label.image = photo
    label.pack()

# Creare fereastra principala
root = tk.Tk()
root.title("PlantMed")

# Dimensiunile imaginii
image_width = 1920
image_height = 1080

# Incarcarea imaginii si redimensionarea la dimensiunile ecranului
background_image = Image.open("pics/fundal.jpg")
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))

# Creare canvas si adaugarea imaginii pe canvas
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill="both", expand=True)
background_photo = ImageTk.PhotoImage(background_image)
canvas.create_image(0, 0, anchor="nw", image=background_photo)

# Creare stil personalizat pentru campurile de introducere
style = ttk.Style()
style.theme_use('clam')
style.configure('Custom.TEntry', fieldbackground='#aed9e0')

# Creare labels, entry, imagini
symptom_entries = []
result_labels = []
image_labels = []
for i in range(1, 6):

    # Labels
    label_symptom = tk.Label(root, text=f"Simptom {i}:", pady=5, font=("Arial", 18), bg="#63ace5", fg="white")
    label_symptom.place(relx=0.05, rely=0.2+0.15*(i-1), relheight=0.05)

    # Entry
    entry_symptom = ttk.Entry(root, style="Custom.TEntry", font=("Arial", 16))
    entry_symptom.place(relx=0.15, rely=0.2+0.15*(i-1), relwidth=0.25, relheight=0.05)
    symptom_entries.append(entry_symptom)

    # After
    result_label = tk.Label(root, text="", wraplength=850, font=("Arial", 16), bg="#63ace5", fg="white")
    result_label.place(relx=0.45, rely=0.18+0.15*(i-1), relheight=0.099)
    result_labels.append(result_label)

    # Hover
    label_symptom.bind("<Enter>", on_enter_label)
    label_symptom.bind("<Leave>", on_leave_label)
    entry_symptom.bind("<Enter>", on_enter_label)
    entry_symptom.bind("<Leave>", on_leave_label)

# Buton de clear
clear_button = tk.Button(root, text="Clear", command=clear_all, width=10, font=("Arial", 16), bg="#63ace5", fg="black", bd=0, relief="flat")
clear_button.place(relx=0.1, rely=0.9, relwidth=0.1, relheight=0.05, anchor="center")
clear_button.bind("<Enter>", on_enter_button)
clear_button.bind("<Leave>", on_leave_button)

# Buton de submit
submit_button = tk.Button(root, text="Submit", command=submit_symptoms, width=10, font=("Arial", 16), bg="#63ace5", fg="black", bd=0, relief="flat")
submit_button.place(relx=0.355, rely=0.9, relwidth=0.1, relheight=0.05, anchor="center")
submit_button.bind("<Enter>", on_enter_button)
submit_button.bind("<Leave>", on_leave_button)

# Titlu
#title_label = tk.Label(root, text="PlantMed", font=("Arial", 36, "bold"), bg="#63ace5", fg="white")
#title_label.place(relx=0.5, rely=0.05, anchor="n")
title_image = Image.open("pics/titlu.png")
title_photo = ImageTk.PhotoImage(title_image)
# Adaugarea imaginii PNG peste imaginea de fundal in canvas
canvas.create_image(root.winfo_screenwidth() // 2, 50, anchor="n", image=title_photo)

# Pornirea buclei principale a interfetei grafice
root.mainloop()
