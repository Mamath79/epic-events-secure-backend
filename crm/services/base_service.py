class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def get_by_id(self, entity_id):
        """
        Récupère une entité par son ID.
        """
        return self.repository.get_by_id(entity_id)

    def get_all(self):
        """
        Récupère toutes les entités.
        """
        return self.repository.get_all()

    def create(self, data):
        """
        Crée une nouvelle entité.
        """
        return self.repository.create(data)

    def update(self, entity_id, new_data):
        """
        Met à jour une entité existante.
        """
        entity = self.repository.get_by_id(entity_id)
        if not entity:
            raise ValueError("Entité introuvable.")
        return self.repository.update(entity, new_data)

    def delete(self, entity_id):
        """
        Supprime une entité.
        """
        entity = self.repository.get_by_id(entity_id)
        if not entity:
            raise ValueError("Entité introuvable.")
        self.repository.delete(entity)
