from flask_restful import Resource
from models.site_model import SiteModel
from flask_jwt_extended import jwt_required


class Site(Resource):
    @staticmethod
    def get(url: str):
        site = SiteModel.find_one(url)
        if site:
            return site.json(), 200
        return {'message': 'Site not found'}, 404

    @staticmethod
    @jwt_required()
    def post(url: str):
        if SiteModel.find_one(url):
            return {'message': f'Site {url} already exists'}, 400
        site = SiteModel(url)
        try:
            site.save_site()
        except (Exception, ValueError):
            return {'message': 'An internal error ocurred trying to save site'}, 500
        return site.json(), 201

    @staticmethod
    @jwt_required()
    def delete(url: str):
        site = SiteModel.find_one(url)
        if site:
            try:
                site.delete_site()
            except (Exception, ValueError):
                return {'message': 'An internal error ocurred trying to delete site'}, 500
            return {'message': f'Site {url} deleted'}, 200
        return {'message': 'Site not found'}, 404
