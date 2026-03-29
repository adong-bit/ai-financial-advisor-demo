"""
基金数据查询模块
使用akshare获取基金数据
"""
import akshare as ak
import pandas as pd
from typing import Dict, List, Optional
import datetime


class FundDataQuery:
    """基金数据查询类"""

    def __init__(self):
        self.fund_list = None

    def get_fund_list(self) -> pd.DataFrame:
        """获取所有基金列表"""
        try:
            # 获取开放式基金列表
            fund_list = ak.fund_open_fund_info_em(
                fund="",
                indicator="单位净值走势"
            )
            return fund_list
        except Exception as e:
            print(f"获取基金列表失败: {e}")
            return pd.DataFrame()

    def search_fund_by_name(self, keyword: str) -> pd.DataFrame:
        """根据关键词搜索基金"""
        try:
            # 获取基金列表
            fund_list = ak.fund_open_fund_info_em(
                fund="",
                indicator="单位净值走势"
            )
            # 筛选包含关键词的基金
            result = fund_list[fund_list['基金名称'].str.contains(keyword, na=False)]
            return result.head(20)
        except Exception as e:
            print(f"搜索基金失败: {e}")
            return pd.DataFrame()

    def get_fund_info(self, fund_code: str) -> Dict:
        """获取基金详细信息"""
        try:
            # 获取基金净值
            fund_nav = ak.fund_open_fund_info_em(
                fund=fund_code,
                indicator="单位净值走势"
            )

            # 获取基金基础信息
            fund_basic = ak.fund_em_fund_info(
                fund=fund_code,
                indicator="单位净值"
            )

            return {
                "code": fund_code,
                "nav_data": fund_nav,
                "basic_info": fund_basic
            }
        except Exception as e:
            print(f"获取基金信息失败: {e}")
            return {}

    def get_fund_performance(self, fund_code: str) -> Dict:
        """获取基金业绩表现"""
        try:
            # 获取基金净值数据
            fund_nav = ak.fund_open_fund_info_em(
                fund=fund_code,
                indicator="单位净值走势"
            )

            if fund_nav.empty:
                return {}

            # 计算简单指标
            nav_values = fund_nav['单位净值'].values
            if len(nav_values) > 1:
                # 简单收益率
                total_return = (nav_values[-1] / nav_values[0] - 1) * 100

                # 最大回撤（简化版）
                max_drawdown = self._calculate_max_drawdown(nav_values)

                return {
                    "total_return": round(total_return, 2),
                    "latest_nav": round(nav_values[-1], 4),
                    "max_drawdown": round(max_drawdown, 2),
                    "data_points": len(nav_values)
                }
            return {}
        except Exception as e:
            print(f"获取基金业绩失败: {e}")
            return {}

    def _calculate_max_drawdown(self, nav_values: List[float]) -> float:
        """计算最大回撤"""
        if len(nav_values) < 2:
            return 0.0

        max_drawdown = 0.0
        peak = nav_values[0]

        for value in nav_values:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown

    def get_recommended_funds(self) -> List[Dict]:
        """获取推荐基金列表（示例数据）"""
        # 这里返回一些知名的指数基金作为示例
        recommended = [
            {
                "code": "110022",
                "name": "易方达消费行业",
                "type": "股票型",
                "risk": "高",
                "category": "卫星-行业主题"
            },
            {
                "code": "000961",
                "name": "天弘沪深300ETF联接",
                "type": "指数型",
                "risk": "高",
                "category": "核心-宽基指数"
            },
            {
                "code": "161725",
                "name": "招商中证白酒指数",
                "type": "指数型",
                "risk": "高",
                "category": "卫星-行业主题"
            },
            {
                "code": "001618",
                "name": "天弘中证电子ETF联接",
                "type": "指数型",
                "risk": "高",
                "category": "卫星-行业主题"
            },
            {
                "code": "005918",
                "name": "天弘创业板ETF联接",
                "type": "指数型",
                "risk": "高",
                "category": "核心-宽基指数"
            }
        ]
        return recommended


# 创建全局实例
fund_query = FundDataQuery()


if __name__ == "__main__":
    # 测试代码
    fq = FundDataQuery()

    # 测试搜索
    print("搜索'沪深300'相关基金:")
    result = fq.search_fund_by_name("沪深300")
    print(result.head())

    # 测试推荐基金
    print("\n推荐基金列表:")
    recs = fq.get_recommended_funds()
    for fund in recs:
        print(fund)
