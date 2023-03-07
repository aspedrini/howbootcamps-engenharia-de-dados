from apis import DaySummaryApi
import datetime

class TestDaySummaryApi:
    def test_get_data(self):
        actual = DaySummaryApi(coin = 'BTC').get_data(date = datetime.date(2021, 1, 1)).get("date")
        expected = '2021-01-01'
        assert actual == expected