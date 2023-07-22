from ranq_app.models import Contestant, Poll, Vote
from django.db.models import Sum
import json

class PopularVote:
    
    @staticmethod
    def rank(id, valid_voters=None):
        contestants = Contestant.objects.filter(poll_id = id)
        
        rank = []
        for contestant in contestants:
            rank.append({
                "name": contestant.name,
                "vote_count": Vote.objects.filter(poll_id = id, contestant_id = contestant.id, voter_id_id__in = valid_voters).aggregate(Sum('rank_value'))['rank_value__sum'] or 0,
            })
            
        # sort by in descending order
        rank.sort(key=lambda x: x["vote_count"], reverse=True)   
        
        # assign position
        for i in range(len(rank)):
            rank[i]["position"] = i + 1
         
        return json.dumps(rank)
        