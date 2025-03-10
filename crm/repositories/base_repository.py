from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, model, session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, entity_id):
        """
        Récupère une entité par son ID.
        """
        return self.session.query(self.model).get(entity_id)

    def get_all(self):
        """
        Récupère toutes les entités.
        """
        return self.session.query(self.model).all()

    def create(self, data):
        """
        Crée une nouvelle entité.
        """
        if isinstance(data, dict):
            entity = self.model(**data)
        else:
            entity = data

        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity, data):
        """
        Met à jour une entité existante.
        """
        for key, value in data.items():
            setattr(entity, key, value)
        self.session.commit()
        return entity

    def delete(self, entity):
        """
        Supprime une entité.
        """
        self.session.delete(entity)
        self.session.commit()
