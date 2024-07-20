import pandas as pd

# Example text from the provided screenshot
text_data = """
DYNAMIC INDUSTRIES LTD.
Member No: D-040/III/L
Category: Dyes and Dyes Intermediates
Year of Established: 1989
Address: GIDC.Plot No. 5501/2Phase 3VatvaAhmedabad - 382445
Phone: 25897221, 25897222
Fax: 25891735
Email: info@dynaind.com
Website: www.dynaind.com
Executive: Harin D. Mamlatdarna
Mobile: 9824052123
Executive: Deepak N. Chokshi
Mobile: 9824000821
Product: Mfg of Acid Dyes, Direct Dyes, Reactive Dyes
Rawmaterial: FC Acid, 6 Nitra, Beta, Gamma Acid
"""

# Split the text into lines and parse the schema
lines = text_data.strip().split("\n")
data = {
    "Company Name": lines[0],
    "Member No": lines[1].split(": ")[1],
    "Category": lines[2].split(": ")[1],
    "Year of Established": lines[3].split(": ")[1],
    "Address": lines[4].split(": ")[1],
    "Phone": lines[5].split(": ")[1],
    "Fax": lines[6].split(": ")[1],
    "Email": lines[7].split(": ")[1],
    "Website": lines[8].split(": ")[1],
    "Executive": [lines[9].split(": ")[1], lines[11].split(": ")[1]],
    "Mobile": [lines[10].split(": ")[1], lines[12].split(": ")[1]],
    "Product": lines[13].split(": ")[1],
    "Rawmaterial": lines[14].split(": ")[1],
}

# Create a DataFrame
df = pd.DataFrame({
    "Company Name": [data["Company Name"]],
    "Member No": [data["Member No"]],
    "Category": [data["Category"]],
    "Year of Established": [data["Year of Established"]],
    "Address": [data["Address"]],
    "Phone": [data["Phone"]],
    "Fax": [data["Fax"]],
    "Email": [data["Email"]],
    "Website": [data["Website"]],
    "Executive": [", ".join(data["Executive"])],
    "Mobile": [", ".join(data["Mobile"])],
    "Product": [data["Product"]],
    "Rawmaterial": [data["Rawmaterial"]],
})

# Save the DataFrame to a CSV file
csv_file_path = "company_data.csv"
df.to_csv(csv_file_path, index=False)

print(f"Data successfully saved to {csv_file_path}")
