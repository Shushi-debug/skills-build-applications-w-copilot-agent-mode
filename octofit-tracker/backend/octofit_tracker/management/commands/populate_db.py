from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import get_test_data

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        test_data = get_test_data()

        # Populate users
        for user_data in test_data['users']:
            User.objects.get_or_create(**user_data)

        # Populate teams
        for team_data in test_data['teams']:
            members = team_data.pop('members')
            team, _ = Team.objects.get_or_create(**team_data)
            team.members.set(User.objects.filter(username__in=members))

        # Populate activities
        for activity_data in test_data['activities']:
            user = User.objects.get(username=activity_data.pop('user'))
            Activity.objects.get_or_create(user=user, **activity_data)

        # Populate leaderboard
        for leaderboard_data in test_data['leaderboard']:
            team = Team.objects.get(name=leaderboard_data.pop('team'))
            Leaderboard.objects.get_or_create(team=team, **leaderboard_data)

        # Populate workouts
        for workout_data in test_data['workouts']:
            Workout.objects.get_or_create(**workout_data)

        self.stdout.write(self.style.SUCCESS('Database populated with test data'))
