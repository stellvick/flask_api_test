from alchemy import db


class SiteModel(db.Model):
    __tablename__ = 'sites'

    site_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80))

    hoteis = db.relationship('HotelModel', backref='site')

    def __init__(self, url: str):
        self.url = url  # type: str

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_one(cls, url: str):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None

    @classmethod
    def find_by_id(cls, site_id: int):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site
        return None

    @classmethod
    def find_all(cls):
        sites = cls.query.all()
        return sites

    def save_site(self):
        db.session.add(self)
        db.session.commit()

    def delete_site(self):
        [hotel.delete_hotel() for hotel in self.hoteis]
        db.session.delete(self)
        db.session.commit()
