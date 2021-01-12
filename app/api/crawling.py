from . import api
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.api.utils.crawler import Crawler
from flask import request

@api.route('/club/<int:club_id>/supply')
# @jwt_required
def crawling(club_id):
    url = request.args.get('url', None)
    
    crawler = Crawler(url).select_crawler()
    options= crawler.run()
    return {'sel_opt_title_list':options[0], 'options':options[1]}
