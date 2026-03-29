"""
资产配置建议引擎
基于核心-卫星策略和现代投资组合理论
"""
from typing import Dict, List
import pandas as pd


class PortfolioAdvisor:
    """资产配置建议引擎"""

    def __init__(self):
        # 风险等级定义
        self.risk_profiles = {
            "conservative": {
                "name": "保守型",
                "equity_ratio": 0.3,
                "bond_ratio": 0.6,
                "cash_ratio": 0.1,
                "description": "追求资产稳健增值，能承受较小波动"
            },
            "balanced": {
                "name": "平衡型",
                "equity_ratio": 0.6,
                "bond_ratio": 0.3,
                "cash_ratio": 0.1,
                "description": "追求资产长期增值，能承受中等波动"
            },
            "aggressive": {
                "name": "进取型",
                "equity_ratio": 0.8,
                "bond_ratio": 0.15,
                "cash_ratio": 0.05,
                "description": "追求资产快速增值，能承受较大波动"
            }
        }

        # 核心配置方案
        self.core_portfolio = {
            "broad_index": {
                "name": "宽基指数",
                "allocation": 0.6,
                "examples": ["沪深300指数", "中证500指数", "标普500指数"],
                "rationale": "获取市场平均收益，分散个股风险"
            },
            "bond_index": {
                "name": "债券指数",
                "allocation": 0.3,
                "examples": ["国债指数", "可转债指数"],
                "rationale": "稳定收益，降低组合波动"
            },
            "international": {
                "name": "国际市场",
                "allocation": 0.1,
                "examples": ["美股QDII", "港股通", "黄金ETF"],
                "rationale": "全球化配置，降低单一市场风险"
            }
        }

        # 卫星配置方向
        self.satellite_themes = {
            "technology": {
                "name": "科技创新",
                "risk": "高",
                "allocation": 0.05,
                "rationale": "把握科技发展趋势，获取超额收益"
            },
            "consumption": {
                "name": "消费升级",
                "risk": "中高",
                "allocation": 0.05,
                "rationale": "受益于消费升级趋势"
            },
            "healthcare": {
                "name": "医疗健康",
                "risk": "中高",
                "allocation": 0.05,
                "rationale": "人口老龄化带来的长期机会"
            },
            "new_energy": {
                "name": "新能源",
                "risk": "高",
                "allocation": 0.05,
                "rationale": "碳中和背景下的产业机遇"
            }
        }

    def assess_risk_profile(self, answers: Dict) -> str:
        """
        根据问卷评估风险类型

        answers: {
            "age": int,
            "investment_experience": str,  # "无"/"1-3年"/"3年以上"
            "risk_tolerance": str,  # "保守"/"平衡"/"进取"
            "investment_goal": str,  # "保值"/"稳健增值"/"快速增值"
            "time_horizon": str  # "1年以内"/"1-3年"/"3年以上"
        }
        """
        score = 0

        # 年龄评分（越年轻分数越高）
        age = answers.get("age", 30)
        if age < 30:
            score += 3
        elif age < 45:
            score += 2
        elif age < 60:
            score += 1
        else:
            score += 0

        # 投资经验评分
        experience = answers.get("investment_experience", "无")
        if experience == "3年以上":
            score += 3
        elif experience == "1-3年":
            score += 2
        else:
            score += 1

        # 风险偏好评分
        risk = answers.get("risk_tolerance", "平衡")
        if risk == "进取":
            score += 3
        elif risk == "平衡":
            score += 2
        else:
            score += 1

        # 投资目标评分
        goal = answers.get("investment_goal", "稳健增值")
        if goal == "快速增值":
            score += 3
        elif goal == "稳健增值":
            score += 2
        else:
            score += 1

        # 时间跨度评分
        horizon = answers.get("time_horizon", "1-3年")
        if horizon == "3年以上":
            score += 3
        elif horizon == "1-3年":
            score += 2
        else:
            score += 1

        # 根据总分判断风险类型
        if score >= 12:
            return "aggressive"
        elif score >= 8:
            return "balanced"
        else:
            return "conservative"

    def generate_portfolio(self, risk_profile: str, invest_amount: float = 100000) -> Dict:
        """
        生成投资组合建议

        Args:
            risk_profile: 风险类型 (conservative/balanced/aggressive)
            invest_amount: 投资金额

        Returns:
            投资组合建议字典
        """
        profile = self.risk_profiles.get(risk_profile, self.risk_profiles["balanced"])

        # 计算核心-卫星配置
        core_amount = invest_amount * 0.75  # 75%核心配置
        satellite_amount = invest_amount * 0.25  # 25%卫星配置

        # 权益类资产分配
        equity_amount = invest_amount * profile["equity_ratio"]

        # 核心配置详情
        core_allocation = []
        for key, config in self.core_portfolio.items():
            amount = core_amount * config["allocation"] * profile["equity_ratio"]
            if profile["equity_ratio"] < 0.5 and key == "bond_index":
                amount = invest_amount * profile["bond_ratio"]

            core_allocation.append({
                "category": config["name"],
                "amount": round(amount, 2),
                "ratio": round(config["allocation"], 2),
                "examples": config["examples"],
                "rationale": config["rationale"]
            })

        # 卫星配置详情
        satellite_allocation = []
        satellite_count = 2 if risk_profile == "conservative" else 4
        themes = list(self.satellite_themes.values())[:satellite_count]

        for theme in themes:
            amount = satellite_amount * (1 / len(themes))
            satellite_allocation.append({
                "category": theme["name"],
                "amount": round(amount, 2),
                "ratio": round(1 / len(themes), 2),
                "risk": theme["risk"],
                "rationale": theme["rationale"]
            })

        return {
            "risk_profile": profile["name"],
            "total_amount": invest_amount,
            "core_satellite_ratio": "75% : 25%",
            "core_allocation": core_allocation,
            "satellite_allocation": satellite_allocation,
            "description": profile["description"],
            "expected_return": self._get_expected_return(risk_profile),
            "expected_volatility": self._get_expected_volatility(risk_profile)
        }

    def _get_expected_return(self, risk_profile: str) -> str:
        """获取预期收益率"""
        returns = {
            "conservative": "5-8%",
            "balanced": "8-12%",
            "aggressive": "12-18%"
        }
        return returns.get(risk_profile, "8-12%")

    def _get_expected_volatility(self, risk_profile: str) -> str:
        """获取预期波动率"""
        volatilities = {
            "conservative": "5-10%",
            "balanced": "10-20%",
            "aggressive": "20-30%"
        }
        return volatilities.get(risk_profile, "10-20%")

    def get_rebalance_suggestion(self, current_portfolio: Dict, target_portfolio: Dict) -> Dict:
        """
        生成再平衡建议

        current_portfolio: 当前持仓
        target_portfolio: 目标配置
        """
        suggestions = {
            "need_rebalance": False,
            "actions": []
        }

        # 简化的再平衡逻辑
        # 实际应用中需要更复杂的对比逻辑

        return suggestions


# 创建全局实例
advisor = PortfolioAdvisor()


if __name__ == "__main__":
    # 测试代码
    pa = PortfolioAdvisor()

    # 测试风险评估
    answers = {
        "age": 30,
        "investment_experience": "1-3年",
        "risk_tolerance": "平衡",
        "investment_goal": "稳健增值",
        "time_horizon": "3年以上"
    }

    risk_profile = pa.assess_risk_profile(answers)
    print(f"风险类型: {risk_profile}")

    # 测试投资组合生成
    portfolio = pa.generate_portfolio(risk_profile, 100000)
    print("\n投资组合建议:")
    print(portfolio)
