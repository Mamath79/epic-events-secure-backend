from datetime import datetime

class Client:
    
    def __init__(self,
                 id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 phone_number: str,
                 creation_date: datetime,
                 update_date: datetime = None,
                 delete_at: datetime = None,
                 companies_id: int = None):
        
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.creation_date = creation_date
        self.update_date = update_date
        self.delete_at = delete_at
        self.companies_id = companies_id  # Lien avec une entreprise

    def __repr__(self):
        return f"<Client {self.first_name} {self.last_name} ({self.email})>"
