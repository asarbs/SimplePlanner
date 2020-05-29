from django.test import TestCase
from PlannerApp.models import Team, Item, Status
import datetime


# Create your tests here.
class ItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods.
        Team.objects.create(name="Test Team")
        Item.objects.create(
        name = "Test item 1",
        wbs_id = "1",
        parent = None,
        priority = 123,
        assignment = None,
        start_date = datetime.datetime(2020, 5, 17),
        end_date = datetime.datetime(2020, 5, 19),
        _planned_start_date = datetime.datetime(2020, 5, 10),
        _planned_end_date = datetime.datetime(2020, 5, 17),
        status = 3,
        team = Team.objects.get(id=1),
        description = "AAAA",
        _progress = 0
        )

        Item.objects.create(
        name = "Test item 2",
        wbs_id = "1.1",
        parent = Item.objects.get(id=1),
        priority = 10,
        assignment = None,
        start_date = datetime.datetime(2020, 5, 17),
        end_date = datetime.datetime(2020, 5, 19),
        _planned_start_date = datetime.datetime(2020, 4, 10),
        _planned_end_date = datetime.datetime(2020, 6, 17),
        status = 3,
        team = Team.objects.get(id=1),
        description = "AAAA",
        _progress = 50
        )

        Item.objects.create(
        name = "Test item 3",
        wbs_id = "1.2",
        parent = Item.objects.get(id=1),
        priority = 1000,
        assignment = None,
        start_date = datetime.datetime(2020, 5, 17),
        end_date = datetime.datetime(2020, 5, 19),
        _planned_start_date = datetime.datetime(2020, 4, 10),
        _planned_end_date = datetime.datetime(2020, 6, 17),
        status = 1,
        team = Team.objects.get(id=1),
        description = "AAAA",
        _progress = 50
        )


        pass

    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_caculate_length(self):
        item = Item.objects.get(id=1)
        self.assertEquals(item.length, 2)

    def test_calculate_ee(self):
        item = Item.objects.get(id=1)
        self.assertEquals(item.effort_estimation, 7)

    def test_cacualte_items_tree_start_date(self):
        item = Item.objects.get(id=1)
        self.assertEquals(item.planned_start_date, datetime.date(2020, 4, 10))

    def test_cacualte_items_tree_end_date(self):
        item = Item.objects.get(id=1)
        self.assertEquals(item.planned_end_date, datetime.date(2020, 6, 17))

    def test_generation_calcualtion(self):
        item = Item.objects.get(id=2) 
        self.assertEquals(item.generation, 1)

    def test_calcualte_root_item_progress(self):
        item = Item.objects.get(id=1)
        self.assertEquals(item.progress, 50)

    def test_calculate_root_item_status(self):
        item = Item.objects.get(id=1)
        self.assertEquals(Status(item.getStatus()), Status.IN_PROGRESS)

    def test_calcualte_priority(self):
        item = Item.objects.get(id=2) 
        self.assertEquals(item.calc_priority(), "0123.0010")



class TeamTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods.
        Team.objects.create(name="Test Team")
        pass

    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_name_of_team(self):
        team = Team.objects.get(id=1)
        team_name = team.name
        self.assertEquals(team_name, 'Test Team')

