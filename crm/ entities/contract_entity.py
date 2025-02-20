from datetime import datetime


class Contract:

    def __init__(self,
                 id: int,
                 total_amount: float,
                 contract_status_id: int,
                 clients_id: int,
                 created_at: datetime,
                 updated_at: datetime = None,
                 deleted_at: datetime = None):
        
        self.id = id
        self.total_amount = total_amount
        self.contract_status_id = contract_status_id  # Référence vers contract_status
        self.clients_id = clients_id  # Référence vers un client
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return f"<Contract {self.id} - Client {self.clients_id}>"
