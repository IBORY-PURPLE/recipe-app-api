"""
Sample tests
"""

from django.test import SimpleTestCase
from app import calc

class CalcTests(SimpleTestCase):
    """Test teh calc modul"""

    def test_add_numbers(self):
        """Test adding numbers together"""
        res = calc.add(5,6)

        self.assertEqual(res, 11)

    #test코드를 먼저 작성하고 app코드를 바꿔가며 테스트를 통과하는 결과를 만든것이 정방향
    def test_subtract_numbers(self):
        """Test subtracting numbers."""
        res = calc.subtract(10, 15)

        self.assertEqual(res, 5)

