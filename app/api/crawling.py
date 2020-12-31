from . import api
from flask import request

@api.route('/club/<int:club_id>/supply')
def crawling(club_id):
    url = request.args.get('url', None)
    
