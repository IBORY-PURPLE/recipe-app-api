"""
Test custom Django management command.
장고가 db와 연결하기 위해서는 약간의 시간적 term이 필요하다.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# patch를 사용해서 Command.check함수를 mock객체로 바꾸어 실제DB에 접속하는 것이 아니라
# 그런 척을 한 것처럼 test를 할 수 있다.
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database if database ready
        check함수가 호출 될 때마다 true값을 반환하게끔 만듦. mock객체 생성.(moc설정하는 단계)
        """
        patched_check.return_value = True

        """
        "python manage.py wait_for-db와 같다고 봐도 무방"
        지금 이 함수가 실행되면서 wait_for_db를 실행하여 check함수가 몇번 호출 됬는지를 검사하려고 하는 듯.
        """
        call_command('wait_for_db')

        """
        setting.py에 저장된 database영역에 가면 default db가 저장되어있는데
        db가 단 한번 호출 되었는지를 확인하는 작업(대신 mocking 작업이라는 것!)
        """
        patched_check.assert_called_once_with(databases=['default'])

    """
    DB가 아직 준비되지 않은 상황을 테스트하는 함수
    매개변수 대입 순서 patch를 적은 역순으로 self는 class매소드이기 때무에 항상 1번!
    class의 인스턴스라고 생각하자.
    """
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test waiting for database when getting OperationError
        처음 2번은 Psycopg2에러를 띄우고 다음 3번은 operationalError를 띄우고 다음에 True를 반환.
        (moc설정하는 단계) 6번째 check함수 호출 때는 true값을 반환하게끔.
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
