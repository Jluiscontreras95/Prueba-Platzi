import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question



class QuestionModelTest(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        '''was_published_recently returns false for questions whose pub_date is in the future'''

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="quien es el mejor director de platzi", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_pass_question(self):
        '''was_published_recently returns false for questions whose pub_date is in the pass'''
        time= timezone.now() - datetime.timedelta(hours=25)
        pass_question = Question(question_text="Cuando terminaste el curso", pub_date=time)
        self.assertIs(pass_question.was_published_recently(), False)

    def test_was_published_recently_with_present_question(self):
        '''was_published_recently returns false for questions whose pub_date is in the present'''
        time= timezone.now()
        present_question = Question(question_text="Aprobaste el curso", pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)


def create_question(question_text, days):
    '''
        Create a question with the given "question_text", and published the given number of days
        offset to now (negative for questions published in the past, positive for questions that have yet to be published)
    '''
    time= timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        '''If no question exist, an appropriate message is displayed'''
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No existen encuestas")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question(self):
        '''Questions with a pub_date in the future are not displayed on the index page.'''
        create_question("Future question", days=30)
        response= self.client.get(reverse("polls:index"))
        self.assertContains(response, "No existen encuestas")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_pass_question(self):
        '''Questions with a pub_date in the past are displayed on the index page.'''
        question = create_question("Past question", days=-10)
        response= self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        ''' Even if both past and future question exists, only past questions are displayed '''
        past_question = create_question("Past question", days=-30)
        future_question = create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[past_question])
        
    def test_two_past_questions(self):
        ''' the questions index page may display multiple questions.'''
        past_question1 = create_question("Past question 1", days=-30)
        past_question2 = create_question("Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[past_question1, past_question2])

    def test_two_future_questions(self):
        ''' the questions index page are not displayed multiple questions.'''
        future_question1 = create_question("Past question 1", days=30)
        future_question2 = create_question("Past question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No existen encuestas")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        ''' The detail view of a question with a pub_date in the future, return a 404 error not found'''
        future_question = create_question("Future question", days=30)
        url = reverse("polls:details", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        ''' The detail view of a question with a pub_date in the past, display the question text'''
        past_question = create_question("Past question", days=-30)
        url = reverse("polls:details", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

        
        
        
        pass

# Create your tests here.
