import os
import unittest
import warnings
import time

from pathlib import Path
from marshmallow.warnings import RemovedInMarshmallow4Warning

from infrastructure import cache_manager
from config import fake_data_1, constants

from domain import IUserDto, ILanguageDto, ICertificationDto, IAchievementDto, IDataDto, IRankingDto


class TestEvaluatorMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  
        # just need to declare those values once for all tests
        # There is warnings from dataclass_json when using default values linked to marshmallow
        # disregard those warnings
        warnings.simplefilter('ignore', category=RemovedInMarshmallow4Warning)

        cls.user = IDataDto(
            user=IUserDto.from_dict(fake_data_1.FAKE_USER),
            languages=ILanguageDto.schema().load(fake_data_1.FAKE_LANGUAGES, many=True),
            certifications=ICertificationDto.schema().load(fake_data_1.FAKE_CERTIF, many=True),
            achievements=IAchievementDto.schema().load(fake_data_1.FAKE_ACHIVEMENTS, many=True),
            rankings=IRankingDto.from_dict(fake_data_1.FAKE_RANKING),
        )

    def setUp(self):
        self.user = TestEvaluatorMethods.user

    def tearDown(self):
        f = Path(constants.CACHE_PATH.format(codingamer="magic"))
        if f.is_file():
            os.remove(str(f))

    def test_get_seconds_since_last_modified(self):
        f = Path(__file__)
        seconds = cache_manager.get_seconds_since_last_modified(str(f))
        self.assertGreater(seconds, 0)
        self.assertLess(seconds, 1e8)

        f = Path(__file__).resolve().parent / "fot_existing_file.foo"
        seconds = cache_manager.get_seconds_since_last_modified(str(f))
        self.assertEqual(seconds, 1e8)

    def test_create_file(self):
        cache_manager.save_data("magic", self.user)

        fake_file = constants.CACHE_PATH.format(codingamer="magic")
        seconds = cache_manager.get_seconds_since_last_modified(fake_file)
        self.assertGreaterEqual(seconds, 0)
        self.assertLess(seconds, 3)  # ensure file is found

    def test_load_data(self):
        cache_manager.save_data("magic", self.user)

        # basic load
        test_data = cache_manager.load_data("magic", expiration_seconds=86400)
        self.assertIsInstance(test_data, IDataDto)

        # load expired data
        time.sleep(2)
        test_data = cache_manager.load_data("magic", expiration_seconds=1)
        self.assertIsNone(test_data)

        # load inexisting
        test_data = cache_manager.load_data("invalid", expiration_seconds=86400)
        self.assertIsNone(test_data)
