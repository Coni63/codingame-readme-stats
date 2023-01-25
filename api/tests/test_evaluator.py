import unittest
import warnings

from marshmallow.warnings import RemovedInMarshmallow4Warning

from domain.evaluator import get_color, get_points_from_rank
from config import constants, fake_data_1, fake_data_2, fake_data_3, fake_data_4

from domain import (
    IUserDto, 
    ILanguageDto, 
    ICertificationDto, 
    IAchievementDto, 
    IDataDto, 
    IRankingDto, 
    ILeaderboardDto
)


class TestEvaluatorMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # just need to declare those values once for all tests
        # There is warnings from dataclass_json when using default values linked to marshmallow
        # disregard those warnings
        warnings.simplefilter('ignore', category=RemovedInMarshmallow4Warning)

        cls.users = [
            IDataDto(
                user=IUserDto.from_dict(fake_data_1.FAKE_USER),
                languages=ILanguageDto.schema().load(fake_data_1.FAKE_LANGUAGES, many=True),
                certifications=ICertificationDto.schema().load(fake_data_1.FAKE_CERTIF, many=True),
                achievements=IAchievementDto.schema().load(fake_data_1.FAKE_ACHIVEMENTS, many=True),
                rankings=IRankingDto.from_dict(fake_data_1.FAKE_RANKING),
                leaderboard=ILeaderboardDto.from_dict(fake_data_1.FAKE_LEADERBOARD),
            ),
            IDataDto(
                user=IUserDto.from_dict(fake_data_2.FAKE_USER),
                languages=ILanguageDto.schema().load(fake_data_2.FAKE_LANGUAGES, many=True),
                certifications=ICertificationDto.schema().load(fake_data_2.FAKE_CERTIF, many=True),
                achievements=IAchievementDto.schema().load(fake_data_2.FAKE_ACHIVEMENTS, many=True),
                rankings=IRankingDto.from_dict(fake_data_2.FAKE_RANKING),
                leaderboard=ILeaderboardDto.from_dict(fake_data_2.FAKE_LEADERBOARD),
            ),
            IDataDto(
                user=IUserDto.from_dict(fake_data_3.FAKE_USER),
                languages=ILanguageDto.schema().load(fake_data_3.FAKE_LANGUAGES, many=True),
                certifications=ICertificationDto.schema().load(fake_data_3.FAKE_CERTIF, many=True),
                achievements=IAchievementDto.schema().load(fake_data_3.FAKE_ACHIVEMENTS, many=True),
                rankings=IRankingDto.from_dict(fake_data_3.FAKE_RANKING),
                leaderboard=ILeaderboardDto.from_dict(fake_data_3.FAKE_LEADERBOARD),
            ),
            IDataDto(
                user=IUserDto.from_dict(fake_data_4.FAKE_USER),
                languages=ILanguageDto.schema().load(fake_data_4.FAKE_LANGUAGES, many=True),
                certifications=ICertificationDto.schema().load(fake_data_4.FAKE_CERTIF, many=True),
                achievements=IAchievementDto.schema().load(fake_data_4.FAKE_ACHIVEMENTS, many=True),
                rankings=IRankingDto.from_dict(fake_data_4.FAKE_RANKING),
                leaderboard=ILeaderboardDto.from_dict(fake_data_4.FAKE_LEADERBOARD),
            ),
        ]

    def setUp(self):
        self.users = TestEvaluatorMethods.users

    def test_get_color(self):

        self.assertEqual(get_color(-100, [2, 4, 6, 8]), constants.COLOR_WOOD)
        self.assertEqual(get_color(1, [2, 4, 6, 8]), constants.COLOR_WOOD)
        self.assertEqual(get_color(2, [2, 4, 6, 8]), constants.COLOR_WOOD)
        self.assertEqual(get_color(3, [2, 4, 6, 8]), constants.COLOR_BRONZE)
        self.assertEqual(get_color(6, [2, 4, 6, 8]), constants.COLOR_SILVER)
        self.assertEqual(get_color(8, [2, 4, 6, 8]), constants.COLOR_GOLD)
        self.assertEqual(get_color(10, [2, 4, 6, 8]), constants.COLOR_LEGEND)

        self.assertEqual(get_color(-100, [2, 4, 6, 8], ascending=False), constants.COLOR_LEGEND)
        self.assertEqual(get_color(1, [2, 4, 6, 8], ascending=False), constants.COLOR_LEGEND)
        self.assertEqual(get_color(2, [2, 4, 6, 8], ascending=False), constants.COLOR_LEGEND)
        self.assertEqual(get_color(3, [2, 4, 6, 8], ascending=False), constants.COLOR_GOLD)
        self.assertEqual(get_color(6, [2, 4, 6, 8], ascending=False), constants.COLOR_SILVER)
        self.assertEqual(get_color(8, [2, 4, 6, 8], ascending=False), constants.COLOR_BRONZE)
        self.assertEqual(get_color(10, [2, 4, 6, 8], ascending=False), constants.COLOR_WOOD)

        with self.assertRaises(ValueError):
            get_color(1, [2, 4, 5, 6, 7, 8])

    def test_get_score_level(self):
        targets = [
            (38, constants.COLOR_LEGEND),
            (56, constants.COLOR_LEGEND),
            (21, constants.COLOR_SILVER),
            (9, constants.COLOR_WOOD),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_level()
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_certificate(self):
        targets = [
            (5, "Legend", constants.COLOR_LEGEND),
            (5, "Legend", constants.COLOR_LEGEND),
            (5, "Wood", constants.COLOR_WOOD),
            (5, "Wood", constants.COLOR_WOOD),
        ]
        for fake_user, (length, target_value, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_certificate()
            self.assertEqual(len(ans), length)
            self.assertEqual(ans[0].value, target_value)
            self.assertEqual(ans[0].color, target_color)

    def test_get_score_best_language(self):
        targets = [
            ("Python 3", constants.COLOR_LEGEND),
            ("C#", constants.COLOR_LEGEND),
            ("Python 3", constants.COLOR_BRONZE),
            ("Swift", constants.COLOR_WOOD),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_best_language()
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_total_solved(self):
        targets = [
            (371, constants.COLOR_LEGEND),
            (759, constants.COLOR_LEGEND),
            (40, constants.COLOR_BRONZE),
            (4, constants.COLOR_WOOD),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_total_solved()
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_achievements(self):
        targets = [
            (127, 146, constants.COLOR_GOLD),
            (137, 146, constants.COLOR_LEGEND),
            (83, 146, constants.COLOR_BRONZE),
            (15, 146, constants.COLOR_WOOD),
        ]
        for fake_user, (target_numerator, target_denominator, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_achievements()
            self.assertIsNone(ans.value)
            self.assertEqual(ans.numerator, target_numerator)
            self.assertEqual(ans.denominator, target_denominator)
            self.assertEqual(ans.color, target_color)

    def test_get_score_rank(self):
        targets = [
            (664, 637326, constants.COLOR_GOLD),
            (4, 640418, constants.COLOR_LEGEND),
            (2411, 640418, constants.COLOR_SILVER),
            (9902, 640418, constants.COLOR_BRONZE),
        ]
        for fake_user, (target_numerator, target_denominator, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_rank()
            self.assertIsNone(ans.value)
            self.assertEqual(ans.numerator, target_numerator)
            self.assertEqual(ans.denominator, target_denominator)
            self.assertEqual(ans.color, target_color)

    def test_get_score_competition(self):
        # ONLINE
        targets = [
            (753, 3509, constants.COLOR_BRONZE),
            (5, 4228, constants.COLOR_LEGEND),
            (391, 2162, constants.COLOR_BRONZE),
            (489, 4955, constants.COLOR_SILVER),
        ]
        for fake_user, (target_numerator, target_denominator, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_competition(online=True)
            self.assertIsNone(ans.value)
            self.assertEqual(ans.numerator, target_numerator)
            self.assertEqual(ans.denominator, target_denominator)
            self.assertEqual(ans.color, target_color)

        # OFFLINE
        targets = [
            (843, 170225, constants.COLOR_LEGEND),
            (3, 3962, constants.COLOR_LEGEND),
            (939, 6267, constants.COLOR_SILVER),
            (693, 6859, constants.COLOR_SILVER),
        ]
        for fake_user, (target_numerator, target_denominator, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_competition(online=False)
            self.assertIsNone(ans.value)
            self.assertEqual(ans.numerator, target_numerator)
            self.assertEqual(ans.denominator, target_denominator)
            self.assertEqual(ans.color, target_color)

    def test_get_score_list_language(self):
        targets = [
            (6, constants.COLOR_LEGEND),  # number of elements and color of the first one
            (6, constants.COLOR_LEGEND),
            (3, constants.COLOR_BRONZE),
            (1, constants.COLOR_WOOD),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = fake_user.get_score_list_language()
            self.assertEqual(len(ans), target_value)
            self.assertEqual(ans[0].color, target_color)

    def test_evaluate(self):
        targets = [
            ("S+", constants.COLOR_LEGEND, 80),
            ("S++", constants.COLOR_LEGEND, 92),
            ("S", constants.COLOR_GOLD, 69),
            ("B", constants.COLOR_BRONZE, 38),
        ]
        for fake_user, (target_value, target_color, target_score) in zip(self.users, targets):
            (active_color, passive_color, score, label) = fake_user.get_main_level()
            self.assertEqual(label, target_value)
            self.assertEqual(active_color, target_color)
            self.assertTrue(abs(score - target_score) < 1)


class TestPointsMethods(unittest.TestCase):

    def test_winner(self):
        N = 5000
        for base in [500, 2000, 5000, 10000]:
            self.assertEqual(get_points_from_rank(1, N, base=base), base)

    def test_last(self):
        N = 5000
        for base in [500, 2000, 5000, 10000]:
            self.assertEqual(get_points_from_rank(N, N, base=base), 1)

    def test_known(self):
        BASE = 2500  # Opti
        self.assertEqual(get_points_from_rank(4098, 6090, base=BASE), 13)
        self.assertEqual(get_points_from_rank(216, 399, base=BASE), 33)
        self.assertEqual(get_points_from_rank(25, 990, base=BASE), 2068)
        self.assertEqual(get_points_from_rank(44, 581, base=BASE), 1401)
        self.assertEqual(get_points_from_rank(60, 358, base=BASE), 521)

        BASE = 5000  # battle bot
        self.assertEqual(get_points_from_rank(420, 2662, base=BASE), 1308)
        self.assertEqual(get_points_from_rank(543, 6260, base=BASE), 2392)
        self.assertEqual(get_points_from_rank(1754, 2815, base=BASE), 25)
        self.assertEqual(get_points_from_rank(843, 170320, base=BASE), 4794)
        self.assertEqual(get_points_from_rank(118, 267, base=BASE), 84)

    def test_fail(self):
        with self.assertRaises(ValueError):
            get_points_from_rank(-2, 5000, base=100)

        with self.assertRaises(ValueError):
            get_points_from_rank(750, 500, base=100)

        with self.assertRaises(ValueError):
            get_points_from_rank(500, 5000, base=0)
