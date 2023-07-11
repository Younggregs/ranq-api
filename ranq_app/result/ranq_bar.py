
import json
from ranq_app.models import Contestant, Vote


class RanqBar(object):
    
    @staticmethod
    def rank(id):
        # get list of contestants
        contestants_queryset = Contestant.objects.filter(poll_id = id)
        contestants = list(map(lambda contestant: contestant, contestants_queryset))
        
        # initialize contestants
        contestants_count = {}
        for contestant in contestants:
            contestants_count[contestant.name] = 0
            
            
        # initialize stack
        stack = []
        
        # initialize bar and bar_limit
        bar = 2
        bar_limit = len(contestants) + 1
        
        # get list of votes
        votes = Vote.objects.filter(poll_id = id)
        
        # create a while loop
        running = True

        while running:
            
            # initialize skip_stack and less than bar checks
            less_than_bar = False
            skip_stack = False
            
            # loop through each contestant
            for contestant in contestants:

                # get contestants vote
                contestants_votes = list(filter(lambda vote: vote.contestant_id_id == contestant.id, votes))
                
                # loop through each vote
                for vote in contestants_votes:
                    # for each vote, check if rank is greater than bar
                    # if >= add 1
                    if vote.rank_value >= bar:
                        contestants_count[contestant.name] += 1

                    else:
                        less_than_bar = True
                        
            # after each rank loop
            # filter and identify candidate with
            # the least votes from dict
            least = {}
            least_index = 0
            least_value = len(contestants) + 3
            for i in range(len(contestants)):
                if contestants_count[contestants[i].name] < least_value:
                    least = contestants[i]
                    least_index = i
                    least_value = contestants_count[contestants[i].name]
                    
            # check if another contestant have the same
            # value with the lowest
            for count in contestants_count:
                # exclude the least
                if count != least.name:
                    if contestants_count[count] == least_value:
                        less_than_bar = False
                        skip_stack = True
                        
            
            if not skip_stack:
                # add the contestant with least value to stack
                stack.append(least)

                # remove contestant from contestants list
                del contestants[least_index]
            
            # increase bar, if all contestants pass the bar
            if not less_than_bar:
                bar += 1

            # if bar_limit is exceeded add all remaining contestants_count
            # to stack and stop
            if bar > bar_limit:
                for contestant in contestants:
                    stack.append(contestant)
                running = False
                
            # if only one candidate remains
            if len(contestants) <= 1:
                stack.append(contestants[0])
                running = False

            # reset contestants_count
            contestants_count = {}
            for contestant in contestants:
                contestants_count[contestant.name] = 0
           
        rank = []     
        # assign position
        stack.reverse()
        for i in range(len(stack)):
            name = "--"
            if stack[i].name == None:
                name = stack[i].name
            rank.append({
                "name": name,
                "vote_count": "--",
                "position": i + 1
            })
            
        return json.dumps(rank)