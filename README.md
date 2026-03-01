-----------------------Smart Invoice System:

Smart Invoice System is a web-based application built with Streamlit that automates invoice tracking, expense categorization, and monthly insights. The system extracts data from PDF invoices, categorizes items automatically, allows users to add custom keywords, and provides an easy-to-use interactive dashboard.

------------------------Features:

1)User Login:

Simple login with username.
Optional purpose of use for tracking.

2) Invoice Upload

Upload PDF invoices in table format only (non-tabular PDFs will not work).
Extracts vendor, date, item, quantity, price automatically.
Categorizes items into predefined categories like Electronics, Food, Utilities, Medical, etc.
Displays a summary of vendor, total amount, and date.

3)Monthly Insights

Generates monthly expense charts automatically.
Allows teaching the system new keywords for categorization.

4)Expense History

Shows all previously uploaded invoices for the logged-in user.
Download history as CSV for offline records.

5)Modern UI Design

Stylish dark theme with gradient colors.
Floating neon dots animation in the background.
Interactive sidebar navigation and hover effects.

6)Data Storage

User data stored in CSV files under the data/ folder.
Categories stored in categories.json and can be updated dynamically.

---------------------How It Works:

1)Login / Start

Enter a username (mandatory) and a purpose of use (optional).
After clicking Start, the user is redirected to the main dashboard.

2)Upload Invoice

*Upload a PDF containing tables. Only tabular invoices are supported.*
The system extracts vendor, date, item, quantity, price.
Each item is categorized automatically based on predefined keywords.
Items and categories are displayed in a table.
Users can download the extracted data as a CSV.

3)Monthly Insights

Displays a bar chart showing total expenses per month.
Users can teach the system new keywords for categorization.
Keywords are saved in categories.json.

4)Expense History

Shows all previously uploaded invoice data for the logged-in user.
CSV download available for offline use.

5)Thank You Page
A fun balloon animation shows appreciation for using the system



---------------------Technologies Used

1)Python 3.10+

2)Streamlit – for the web interface.

3)Pandas – for data handling.

4)pdfplumber – to extract tables from PDF invoices.

5)PyPDF2 – dependency for PDF handling.

6)OpenPyXL – optional for Excel exports.



-----------------------Smartinvoice
│
├─ app.py                 # Main Streamlit application                 
├─ data/                  # Stores user CSV files
└─ requirements.txt       # Project dependencies
