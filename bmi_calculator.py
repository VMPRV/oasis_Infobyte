import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import csv
import os


# Functions for BMI Calculation and Categorization
def calculate_bmi(weight, height):
    return weight / (height ** 2)


def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


def save_bmi_data(weight, height, bmi, category):
    file_exists = os.path.isfile('bmi_data.csv')
    with open('bmi_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Weight (kg)', 'Height (m)', 'BMI', 'Category'])
        writer.writerow([weight, height, bmi, category])


def view_history():
    if not os.path.isfile('bmi_data.csv'):
        messagebox.showinfo("No Data", "No historical data available.")
        return

    dates, bmi_values = [], []

    with open('bmi_data.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            bmi_values.append(float(row['BMI']))

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(bmi_values)), bmi_values, marker='o')
    plt.title('BMI History')
    plt.xlabel('Record Number')
    plt.ylabel('BMI')
    plt.grid(True)
    plt.show()


def calculate_and_display_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid Input", "Weight and height must be positive numbers.")
            return

        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)

        result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")
        save_bmi_data(weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and height.")


# GUI Setup
app = tk.Tk()
app.title("BMI Calculator")

tk.Label(app, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=10)
weight_entry = tk.Entry(app)
weight_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(app, text="Height (m):").grid(row=1, column=0, padx=10, pady=10)
height_entry = tk.Entry(app)
height_entry.grid(row=1, column=1, padx=10, pady=10)

calculate_button = tk.Button(app, text="Calculate BMI", command=calculate_and_display_bmi)
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

result_label = tk.Label(app, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

history_button = tk.Button(app, text="View History", command=view_history)
history_button.grid(row=4, column=0, columnspan=2, pady=10)

app.mainloop()
