"""
AI对话模块
支持多种AI模型（minimax、Claude、OpenAI）
"""
import os
from typing import Optional, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class AIAssistant:
    """AI助手类"""

    def __init__(self, model_type: str = "openai"):
        """
        初始化AI助手

        Args:
            model_type: 模型类型 ("minimax", "claude", "openai")
        """
        self.model_type = model_type
        self.client = None
        self._init_client()

    def _init_client(self):
        """初始化AI客户端"""
        if self.model_type == "minimax":
            # minimax API设置
            self.api_key = os.getenv("MINIMAX_API_KEY")
            self.group_id = os.getenv("MINIMAX_GROUP_ID")
        elif self.model_type == "claude":
            try:
                import anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if api_key:
                    self.client = anthropic.Anthropic(api_key=api_key)
                else:
                    print("提示: 未配置ANTHROPIC_API_KEY，将使用内置规则回复")
            except ImportError:
                print("警告: 未安装anthropic库，请运行: pip install anthropic")
        else:  # openai
            try:
                from openai import OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    base_url = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
                    self.client = OpenAI(api_key=api_key, base_url=base_url)
                else:
                    print("提示: 未配置OPENAI_API_KEY，将使用内置规则回复")
            except ImportError:
                print("警告: 未安装openai库，请运行: pip install openai")

    def chat(self, user_message: str, context: Optional[str] = None) -> str:
        """
        与AI对话

        Args:
            user_message: 用户消息
            context: 上下文信息（可选）

        Returns:
            AI回复
        """
        if self.client is None:
            return self._get_fallback_response(user_message)

        try:
            if self.model_type == "claude":
                return self._chat_with_claude(user_message, context)
            else:
                return self._chat_with_openai(user_message, context)
        except Exception as e:
            print(f"AI调用失败: {e}")
            return self._get_fallback_response(user_message)

    def _chat_with_claude(self, user_message: str, context: Optional[str] = None) -> str:
        """使用Claude进行对话"""
        system_prompt = self._get_system_prompt()
        if context:
            system_prompt += f"\n\n当前用户画像:\n{context}"

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return message.content[0].text

    def _chat_with_openai(self, user_message: str, context: Optional[str] = None) -> str:
        """使用OpenAI进行对话"""
        system_prompt = self._get_system_prompt()
        if context:
            system_prompt += f"\n\n当前用户画像:\n{context}"

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一位专业的智能投顾助手，基于买方投顾理念为用户提供服务。

核心理念：
1. 以客户利益为中心，而非销售导向
2. 基于现代投资组合理论(MPT)和核心-卫星策略
3. 强调长期投资和资产配置
4. 注重风险管理和投资者适当性

服务原则：
- 始终提示投资风险
- 不承诺保本保收益
- 根据用户风险承受能力提供建议
- 用通俗易懂的语言解释专业概念
- 不提供具体买卖时点建议

回答风格：
- 专业、客观、易懂
- 有理论支撑（如MPT、行为金融学）
- 适合基金投资新手
- 注重投资者教育

请以友好、专业的态度回答用户问题。"""

    def _get_fallback_response(self, user_message: str) -> str:
        """获取备用回复（当AI服务不可用时）"""
        # 简单的规则匹配
        user_msg = user_message.lower()

        if "风险" in user_msg or "保守" in user_msg:
            return """根据投资组合理论，风险主要分为：
1. 市场风险：整个市场波动带来的风险
2. 个股风险：单一股票或基金的风险
3. 流动性风险：无法及时变现的风险

通过资产配置可以分散风险，建议采用核心-卫星策略：
- 核心（75%）：宽基指数+债券，获取市场平均收益
- 卫星（25%）：行业主题基金，追求超额收益"""

        elif "配置" in user_msg or "组合" in user_msg:
            return """资产配置是投资成功的核心。建议采用"核心-卫星"策略：

**核心配置（75%）**
- 宽基指数基金（60%）：如沪深300、中证500
- 债券基金（30%）：如国债指数、可债指数
- 国际配置（10%）：如QDII基金

**卫星配置（25%）**
- 科技创新（5%）
- 消费升级（5%）
- 医疗健康（5%）
- 新能源（5%）
- 其他机会性配置（5%）

配置比例应根据您的风险承受能力调整。"""

        elif "新手" in user_msg or "开始" in user_msg:
            return """欢迎开始投资之旅！作为新手，建议您：

1. **先做风险评估**：了解自己的风险承受能力
2. **从小额开始**：可以先尝试指数基金定投
3. **长期投资**：基金投资适合3年以上的持有期
4. **学习基础知识**：了解不同类型基金的特点
5. **不要追涨杀跌**：坚持定投，平滑市场波动

我可以帮您做风险评估和配置建议，您想从哪里开始？"""

        else:
            return """感谢您的提问！作为智能投顾助手，我可以帮您：

✅ 风险评估和画像分析
✅ 资产配置建议
✅ 基金筛选和推荐
✅ 投资组合优化
✅ 投资知识普及

请问您想了解哪方面的内容？"""

    def explain_portfolio(self, portfolio: dict) -> str:
        """解释投资组合"""
        explanation = f"""
根据您的{portfolio['risk_profile']}风险类型，我为您设计了以下投资组合：

【整体配置】
- 核心:卫星 = {portfolio['core_satellite_ratio']}
- 预期年化收益: {portfolio['expected_return']}
- 预期波动率: {portfolio['expected_volatility']}

【核心配置】（追求稳健收益）
"""
        for item in portfolio['core_allocation']:
            explanation += f"- {item['category']}: {item['ratio']*100}% ({item['rationale']})\n"

        explanation += "\n【卫星配置】（追求超额收益）\n"
        for item in portfolio['satellite_allocation']:
            explanation += f"- {item['category']}: {item['ratio']*100}% (风险等级:{item['risk']})\n"

        explanation += f"\n{portfolio['description']}"

        return explanation


# 创建全局实例
ai_assistant = AIAssistant(model_type="openai")  # 默认使用OpenAI，可以改为"claude"或"minimax"


if __name__ == "__main__":
    # 测试代码
    ai = AIAssistant(model_type="openai")

    # 测试对话
    response = ai.chat("我是投资新手，应该怎么开始？")
    print(response)
