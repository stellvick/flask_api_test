from alchemy import db


class HotelModel(db.Model):
    __tablename__ = 'hoteis'

    hotel_id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(80))
    estrelas = db.Column(db.Float(precision=1))
    diaria = db.Column(db.Float(precision=2))
    cidade = db.Column(db.String(40))

    def __init__(self, hotel_id: str, nome: str, estrelas: float, diaria: float, cidade: str):
        self.hotel_id = hotel_id  # type: str
        self.nome = nome  # type: str
        self.estrelas = estrelas  # type: float
        self.diaria = diaria  # type: float
        self.cidade = cidade  # type: str

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }

    @classmethod
    def find_hotel(cls, hotel_id: str):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        db.session.add(self)
        db.session.commit()
