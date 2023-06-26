from ranq.celery import app
from ranq_app.models import Poll, Voter, User, Result
from ranq_app.lib.email import Email
from ranq_app.result.popular_vote import PopularVote
from ranq_app.result.ranq_bar import RanqBar

@app.task
def result_task(id):

    # do nothing is poll is already completed
    if Poll.objects.get(pk = id).status == "completed":
        return 
    
    poll = Poll.objects.get(pk = id)
    poll.status = "completed"
    poll.save()

    voters = Voter.objects.filter(poll_id = poll, voted = True)
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
            Email.send(voter.email, poll.token, 'result', 3, poll.title)
        except:
            pass
        
    # create results
    result = Result()
    result.poll_id = poll
    result.popular_vote = PopularVote.rank(id)
    result.rank_raise_bar = RanqBar.rank(id)
    result.save()