from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Comparison:
    value: float
    percentage: Optional[float]

@dataclass
class EarningsData:
    amount: float
    comparison: Optional[Comparison] = None

@dataclass
class DashboardData:
    today: EarningsData
    yesterday: EarningsData
    last_7_days: EarningsData
    this_month: EarningsData

class AdSenseDataManager:
    def __init__(self):
        from adsense_api import get_adsense_data
        self._get_adsense_data = get_adsense_data
        self._last_update = None
        self._cache = None

    def get_dashboard_data(self) -> DashboardData:
        """최신 대시보드 데이터 반환"""
        try:
            raw_data = self._get_adsense_data()
            
            return DashboardData(
                today=EarningsData(
                    amount=raw_data['today']['earnings'],
                    comparison=Comparison(**raw_data['today']['comparison'])
                ),
                yesterday=EarningsData(
                    amount=raw_data['yesterday']['earnings'],
                    comparison=Comparison(**raw_data['yesterday']['comparison'])
                ),
                last_7_days=EarningsData(
                    amount=raw_data['last_7_days']['earnings']
                ),
                this_month=EarningsData(
                    amount=raw_data['this_month']['earnings'],
                    comparison=Comparison(**raw_data['this_month']['comparison'])
                )
            )
        except Exception as e:
            print(f"Error fetching AdSense data: {e}")
            return self._get_empty_data()

    def _get_empty_data(self) -> DashboardData:
        """에러 상황을 위한 빈 데이터 생성"""
        empty_comparison = Comparison(value=0.0, percentage=0.0)
        empty_earnings = EarningsData(amount=0.0, comparison=empty_comparison)
        return DashboardData(
            today=empty_earnings,
            yesterday=empty_earnings,
            last_7_days=EarningsData(amount=0.0),
            this_month=empty_earnings
        )