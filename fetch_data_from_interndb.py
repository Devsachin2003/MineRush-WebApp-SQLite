import sqlite3

def get_company_email_by_application_id(application_id):
    """Fetch the company's email associated with the given application_id."""
    conn = sqlite3.connect('users.db')  # Replace with your actual DB file path
    cursor = conn.cursor()
    
    # Query the database to get the company email for a given application ID
    cursor.execute("SELECT company_email FROM internship_applications WHERE id = ?", (application_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    # If a result is found, return the email, otherwise return None
    return result[0] if result else None
