import json
from django.test import TestCase

from ranq_app.models import Contestant, Poll, User, Vote, Voter
from ranq_app.result.popular_vote import PopularVote
from ranq_app.result.ranq_bar import RanqBar

class ResultTestCase(TestCase):
    def setUp(self):
        # create user 
        User.objects.create(email="test@test.com", first_name="test", last_name="test", username="test", password="test")
        user = User.objects.get(email="test@test.com")
        
        # create poll
        Poll.objects.create(title="test", description="test", created_by=user, status="completed", token="test", contestants=["a", "b", "c", "d"], voters=["test1", "test2", "test3", "test4"])
        poll = Poll.objects.get(title="test")
        
        # create contestants
        Contestant.objects.create(poll_id=poll, name="a")
        Contestant.objects.create(poll_id=poll, name="b")
        Contestant.objects.create(poll_id=poll, name="c")
        Contestant.objects.create(poll_id=poll, name="d")
        a = Contestant.objects.get(name="a")
        b = Contestant.objects.get(name="b")
        c = Contestant.objects.get(name="c")
        d = Contestant.objects.get(name="d")
        
        # create voters
        Voter.objects.create(poll_id=poll, email="test1", token="test1", voted=True)
        Voter.objects.create(poll_id=poll, email="test2", token="test1", voted=True)
        Voter.objects.create(poll_id=poll, email="test3", token="test1", voted=True)
        Voter.objects.create(poll_id=poll, email="test4", token="test1", voted=True)
        test1 = Voter.objects.get(email="test1")
        test2 = Voter.objects.get(email="test2")
        test3 = Voter.objects.get(email="test3")
        test4 = Voter.objects.get(email="test4")
        
        # create votes
        # 1
        Vote.objects.create(poll_id=poll, contestant_id=a, voter_id=test1, rank_value=4)
        Vote.objects.create(poll_id=poll, contestant_id=a, voter_id=test2, rank_value=1)
        Vote.objects.create(poll_id=poll, contestant_id=a, voter_id=test3, rank_value=3)
        Vote.objects.create(poll_id=poll, contestant_id=a, voter_id=test4, rank_value=1)
        
        # 2
        Vote.objects.create(poll_id=poll, contestant_id=b, voter_id=test1, rank_value=3)
        Vote.objects.create(poll_id=poll, contestant_id=b, voter_id=test2, rank_value=3)
        Vote.objects.create(poll_id=poll, contestant_id=b, voter_id=test3, rank_value=1)
        Vote.objects.create(poll_id=poll, contestant_id=b, voter_id=test4, rank_value=4)
        
        # 3
        Vote.objects.create(poll_id=poll, contestant_id=c, voter_id=test1, rank_value=2)
        Vote.objects.create(poll_id=poll, contestant_id=c, voter_id=test2, rank_value=4)
        Vote.objects.create(poll_id=poll, contestant_id=c, voter_id=test3, rank_value=4)
        Vote.objects.create(poll_id=poll, contestant_id=c, voter_id=test4, rank_value=3)
        
        # 4
        Vote.objects.create(poll_id=poll, contestant_id=d, voter_id=test1, rank_value=1)
        Vote.objects.create(poll_id=poll, contestant_id=d, voter_id=test2, rank_value=2)
        Vote.objects.create(poll_id=poll, contestant_id=d, voter_id=test3, rank_value=2)
        Vote.objects.create(poll_id=poll, contestant_id=d, voter_id=test4, rank_value=2)
    
    def test_popular_vote(self):
        """Popular vote should be calculated correctly"""
        
        user = User.objects.get(email="test@test.com")
        poll = Poll.objects.get(title="test")
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(poll.title, 'test')
        self.assertEqual(PopularVote.rank(poll.id), json.dumps([{"name": "c", "vote_count": 13, "position": 1}, {"name": "b", "vote_count": 11, "position": 2}, {"name": "a", "vote_count": 9, "position": 3}, {"name": "d", "vote_count": 7, "position": 4}]))
        
    def test_ranq_bar(self):
        """Popular vote should be calculated correctly"""
        
        user = User.objects.get(email="test@test.com")
        poll = Poll.objects.get(title="test")
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(poll.title, 'test')
        self.assertEqual(RanqBar.rank(poll.id), json.dumps([{'name': 'c', 'vote_count': '--', 'position': 1}, {'name': 'b', 'vote_count': '--', 'position': 2}, {'name': 'd', 'vote_count': '--', 'position': 3}, {'name': 'a', 'vote_count': '--', 'position': 4}]))