import asyncio
import unittest
import warnings

from marshmallow.warnings import RemovedInMarshmallow4Warning
from domain.i_data import IDataDto
from application.user_data import get_all_data
from config import fake_data

class TestGetAllDataMethods(unittest.IsolatedAsyncioTestCase):
    """
    This is more an integration test
    It's hard to mock the external API and as a result test the application level
    """
    def setUp(self):
        # There is warnings from dataclass_json when using default values linked to marshmallow
        # disregard those warnings
        warnings.simplefilter('ignore', category=RemovedInMarshmallow4Warning)

        # There is warnings from asyncio with ResourceWarning: Enable tracemalloc to get the object allocation traceback
        warnings.simplefilter("ignore", category=ResourceWarning)

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.loop = asyncio.get_event_loop_policy().get_event_loop()

    def tearDown(self) -> None:
        self.loop.close()

    async def test_fake_data(self):
        # https://www.codingame.com/profile/de015f1a510d60cdcd0551896a34c709188072
        codingamer = "magic"
        userId = 0

        ans = await get_all_data(codingamer)

        self.assertEqual(ans.user.codingamer.userId, userId)
        self.assertIsInstance(ans, IDataDto)
        self.assertEqual(len(ans.certifications), len(fake_data.FAKE_CERTIF))
        self.assertEqual(len(ans.languages), len(fake_data.FAKE_LANGUAGES))
        self.assertEqual(len(ans.rankings.puzzles), len(fake_data.FAKE_RANKING["puzzles"]))
        self.assertEqual(len(ans.achievements), len(fake_data.FAKE_ACHIVEMENTS))

    async def test_my_user_data(self):
        # https://www.codingame.com/profile/de015f1a510d60cdcd0551896a34c709188072
        codingamer = "de015f1a510d60cdcd0551896a34c709188072"
        userId = 270881

        ans = await get_all_data(codingamer)

        self.assertEqual(ans.user.codingamer.userId, userId)
        self.assertIsInstance(ans, IDataDto)

    async def test_other_user_data(self):
        # https://www.codingame.com/profile/8374201b6f1d19eb99d61c80351465b65150051
        codingamer = "8374201b6f1d19eb99d61c80351465b65150051"
        userId = 1500515

        ans = await get_all_data(codingamer)

        self.assertEqual(ans.user.codingamer.userId, userId)
        self.assertIsInstance(ans, IDataDto)

    async def test_unknown_user_data(self):
        codingamer = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        with self.assertRaises(ValueError):
            await get_all_data(codingamer)

    async def test_invalid_user_data(self):        
        codingamer = "thisisinvalidcodingamer"

        with self.assertRaises(ValueError):
            await get_all_data(codingamer)

if __name__ == '__main__':
    unittest.main()