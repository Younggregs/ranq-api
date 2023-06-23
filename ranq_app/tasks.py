from ranq.celery import app
from ranq_app.models import Poll, Voter, User, Result
from ranq_app.lib.email import Email
from ranq_app.result.rank import Rank

@app.task
def result_task(id):

    # do nothing is poll is already completed
    if Poll.objects.get(pk = id).status == "completed":
        return 
    
    poll = Poll.objects.get(pk = id)
    poll.status = "completed"
    poll.save()

    voters = Voter.objects.filter(poll_id = poll)
    user = User.objects.get(email = poll.created_by)
    
    # send email to poll creator
    try:
         Email.send(user.email, poll.token, 'result', 3, poll.title)
    except:
        pass
    
    # send email to voters
    for voter in voters:
        # send email
        try:
            # if voter voted
            if voter.voted:
                Email.send(voter.email, poll.token, 'result', 3, poll.title)
        except:
            pass
        
    # create results
    result = Result()
    result.poll_id = poll
    
    # calculate popular vote
    result.popular_vote = Rank.popular_vote(id)
    result.save()