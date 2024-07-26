from alchemy import db


class HotelModel(db.Model):
    __tablename__ = 'hoteis'

    hotel_id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(80))
    estrelas = db.Column(db.Float(precision=1))
    diaria = db.Column(db.Float(precision=2))
    cidade = db.Column(db.String(40))
    site_id = db.Column(db.Integer, db.ForeignKey('sites.site_id'))

    def __init__(self, hotel_id: str, nome: str, estrelas: float, diaria: float, cidade: str, site_id: int):
        self.hotel_id = hotel_id  # type: str
        self.nome = nome  # type: str
        self.estrelas = estrelas  # type: float
        self.diaria = diaria  # type: float
        self.cidade = cidade  # type: str
        self.site_id = site_id  # type: int

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id
        }

    @classmethod
    def find_one(cls, hotel_id: str):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    @classmethod
    def find_all(cls):
        hotels = cls.query.all()
        return hotels

    def save_hotel(self):
        db.session.add(self)
        db.session.commit()

    def update_hotel(self, nome: str, estrelas: float, diaria: float, cidade: str):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.save_hotel()

    def delete_hotel(self):
        db.session.delete(self)
        db.session.commit()
