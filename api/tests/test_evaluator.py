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
    get_main_level
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

    def test_get_score_level(self):
        targets = [
            (38, constants.COLOR_LEGEND),
            (38, constants.COLOR_LEGEND),
            (38, constants.COLOR_LEGEND),
            (38, constants.COLOR_LEGEND),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_level(fake_user.user)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_certificate(self):
        targets = [
            (5, "LEGEND", constants.COLOR_LEGEND),
            (5, "LEGEND", constants.COLOR_LEGEND),
            (5, "LEGEND", constants.COLOR_LEGEND),
            (5, "LEGEND", constants.COLOR_LEGEND),
        ]
        for fake_user, (length, target_value, target_color) in zip(self.users, targets):
            ans = get_score_certificate(fake_user.certifications)
            self.assertEqual(len(ans), length)
            self.assertEqual(ans[0].value, target_value)
            self.assertEqual(ans[0].color, target_color)

    def test_get_score_best_language(self):
        targets = [
            ("Python 3", constants.COLOR_LEGEND),
            ("Python 3", constants.COLOR_LEGEND),
            ("Python 3", constants.COLOR_LEGEND),
            ("Python 3", constants.COLOR_LEGEND),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_best_language(fake_user.languages)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_total_solved(self):
        targets = [
            (371, constants.COLOR_LEGEND),
            (371, constants.COLOR_LEGEND),
            (371, constants.COLOR_LEGEND),
            (371, constants.COLOR_LEGEND),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_total_solved(fake_user.languages)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_achievements(self):
        targets = [
            ("127/146", constants.COLOR_GOLD),
            ("127/146", constants.COLOR_GOLD),
            ("127/146", constants.COLOR_GOLD),
            ("127/146", constants.COLOR_GOLD),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_achievements(fake_user.achievements)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_rank(self):
        targets = [
            ("664/637326", constants.COLOR_LEGEND),
            ("664/637326", constants.COLOR_LEGEND),
            ("664/637326", constants.COLOR_LEGEND),
            ("664/637326", constants.COLOR_LEGEND),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_rank(fake_user.user)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_score_competition(self):
        # ONLINE
        targets = [
            ("753/3509", constants.COLOR_SILVER),
            ("753/3509", constants.COLOR_SILVER),
            ("753/3509", constants.COLOR_SILVER),
            ("753/3509", constants.COLOR_SILVER),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_competition(fake_user.rankings, online=True)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

        # OFFLINE
        targets = [
            ("843/170225", constants.COLOR_LEGEND),
            ("843/170225", constants.COLOR_LEGEND),
            ("843/170225", constants.COLOR_LEGEND),
            ("843/170225", constants.COLOR_LEGEND),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_score_competition(fake_user.rankings, online=False)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)

    def test_get_main_level(self):
        targets = [
            ("S", constants.COLOR_LEGEND),
            ("S", constants.COLOR_LEGEND),
            ("S", constants.COLOR_LEGEND),
            ("S", constants.COLOR_LEGEND),
        ]
        for fake_user, (target_value, target_color) in zip(self.users, targets):
            ans = get_main_level(fake_user)
            self.assertEqual(ans.value, target_value)
            self.assertEqual(ans.color, target_color)
