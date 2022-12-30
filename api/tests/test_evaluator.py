import unittest
import warnings

from marshmallow.warnings import RemovedInMarshmallow4Warning

from application.evaluator import (
    get_score_level, 
    get_score_certificate, 
    get_score_best_language, 
    get_score_total_solved, 
    get_score_achievements, 
    get_score_rank, 
    get_score_competition,
    get_main_level,
    get_color
)
from config import constants, fake_data_1, fake_data_2, fake_data_3, fake_data_4

from domain.i_user_info import IUserDto
from domain.i_language import ILanguageDto
from domain.i_certification import ICertificationDto
from domain.i_achievement import IAchievementDto
from domain.i_data import IDataDto
from domain.i_ranking import IRankingDto


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
            ),
            IDataDto(
                user=IUserDto.from_dict(fake_data_2.FAKE_USER),
                languages=ILanguageDto.schema().load(fake_data_2.FAKE_LANGUAGES, many=True),
                certifications=ICertificationDto.schema().load(fake_data_2.FAKE_CERTIF, many=True),
                achievements=IAchievementDto.schema().load(fake_data_2.FAKE_ACHIVEMENTS, many=True),
                rankings=IRankingDto.from_dict(fake_data_2.FAKE_RANKING),
            ),
            IDataDto(
                user=IUserDto.from_dict(fake_data_3.FAKE_USER),
                languages=ILanguageDto.schema().load(fake_data_3.FAKE_LANGUAGES, many=True),
                certifications=ICertificationDto.schema().load(fake_data_3.FAKE_CERTIF, many=True),
                achievements=IAchievementDto.schema().load(fake_data_3.FAKE_ACHIVEMENTS, many=True),
                rankings=IRankingDto.from_dict(fake_data_3.FAKE_RANKING),
            ),
            IDataDto(
                user=IUserDto.from_dict(fake_data_4.FAKE_USER),
                languages=ILanguageDto.schema().load(fake_data_4.FAKE_LANGUAGES, many=True),
                certifications=ICertificationDto.schema().load(fake_data_4.FAKE_CERTIF, many=True),
                achievements=IAchievementDto.schema().load(fake_data_4.FAKE_ACHIVEMENTS, many=True),
                rankings=IRankingDto.from_dict(fake_data_4.FAKE_RANKING),
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
            ans = get_score_level(fake_user.user)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_certificate(self):
        targets = [
            (5, "LEGEND", constants.COLOR_LEGEND),
            (5, "LEGEND", constants.COLOR_LEGEND),
            (5, "WOOD", constants.COLOR_WOOD),
            (5, "WOOD", constants.COLOR_WOOD),
        ]
        for fake_user, (length, target_value, target_color) in zip(self.users, targets):
            ans = get_score_certificate(fake_user.certifications)
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
            ans = get_score_best_language(fake_user.languages)
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
            ans = get_score_total_solved(fake_user.languages)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_achievements(self):
        targets = [
            ("127/146", constants.COLOR_GOLD),
            ("137/146", constants.COLOR_LEGEND),
            ("83/146", constants.COLOR_BRONZE),
            ("15/146", constants.COLOR_WOOD),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_achievements(fake_user.achievements)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_rank(self):
        targets = [
            ("664/637326", constants.COLOR_GOLD),
            ("4/640418", constants.COLOR_LEGEND),
            ("2411/640418", constants.COLOR_SILVER),
            ("9902/640418", constants.COLOR_BRONZE),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_rank(fake_user.user)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_competition(self):
        # ONLINE
        targets = [
            ("753/3509", constants.COLOR_BRONZE),
            ("5/4228", constants.COLOR_LEGEND),
            ("391/2162", constants.COLOR_BRONZE),
            ("489/4955", constants.COLOR_SILVER),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_competition(fake_user.rankings, online=True)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

        # OFFLINE
        targets = [
            ("843/170225", constants.COLOR_LEGEND),
            ("3/3962", constants.COLOR_LEGEND),
            ("939/6267", constants.COLOR_SILVER),
            ("693/6859", constants.COLOR_SILVER),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_competition(fake_user.rankings, online=False)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_evaluate(self):
        targets = [
            ("S+", constants.COLOR_LEGEND, 89),
            ("S++", constants.COLOR_LEGEND, 100),
            ("B", constants.COLOR_BRONZE, 42),
            ("C", constants.COLOR_WOOD, 19),
        ]
        for fake_user, (target_value, target_color, target_score) in zip(self.users, targets):
            level_value = get_score_level(fake_user.user)
            certif_value = get_score_certificate(fake_user.certifications)
            top_language_value = get_score_best_language(fake_user.languages)
            puzzle_solved_value = get_score_total_solved(fake_user.languages)
            achievements_value = get_score_achievements(fake_user.achievements)
            rank_value = get_score_rank(fake_user.user)
            comp_value = get_score_competition(fake_user.rankings, online=False)

            (active_color, passive_color, score, label) = get_main_level(
                level_value,
                certif_value,
                top_language_value,
                puzzle_solved_value,
                achievements_value,
                rank_value,
                comp_value
            )
            self.assertEqual(label, target_value)
            self.assertEqual(active_color, target_color)
            self.assertTrue(abs(score - target_score) < 1)
