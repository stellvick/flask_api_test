from flask_restful import Resource
from models.site_model import SiteModel


class Sites(Resource):
    @staticmethod
    def get():
        sites = SiteModel.find_all()
        return {'sites': [site.json() for site in sites]}, 200
