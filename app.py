"""
AI智能投顾助手 - Streamlit主应用
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fund_data import fund_query
from portfolio_advisor import advisor
from ai_assistant import ai_assistant

# 页面配置
st.set_page_config(
    page_title="AI智能投顾助手",
    page_icon="📈",
    layout="wide"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # 标题
    st.markdown('<h1 class="main-header">📈 AI智能投顾助手</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # 侧边栏
    with st.sidebar:
        st.header("🎯 功能导航")
        page = st.radio(
            "选择功能",
            ["🏠 首页", "🔍 风险评估", "💼 资产配置", "📊 基金筛选", "🤖 AI顾问", "📚 投资知识"]
        )

        st.markdown("---")
        st.info("""
        **核心理念**
        - 核心-卫星策略
        - 买方投顾导向
        - 以客户利益为中心
        - 长期投资陪伴
        """)

    # 首页
    if page == "🏠 首页":
        show_homepage()

    # 风险评估
    elif page == "🔍 风险评估":
        show_risk_assessment()

    # 资产配置
    elif page == "💼 资产配置":
        show_portfolio_allocation()

    # 基金筛选
    elif page == "📊 基金筛选":
        show_fund_selection()

    # AI顾问
    elif page == "🤖 AI顾问":
        show_ai_advisor()

    # 投资知识
    elif page == "📚 投资知识":
        show_investment_knowledge()


def show_homepage():
    """首页"""
    st.markdown("## 🌟 欢迎使用AI智能投顾助手")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("核心理念", "核心-卫星策略")
        st.markdown("""
        **75%核心配置**
        - 宽基指数
        - 债券指数
        - 国际配置

        **25%卫星配置**
        - 行业主题
        - 机会性配置
        """)

    with col2:
        st.metric("服务特色", "买方投顾导向")
        st.markdown("""
        ✓ 以客户利益为中心
        ✓ 不推荐销售导向产品
        ✓ 强调风险控制
        ✓ 长期陪伴服务
        """)

    with col3:
        st.metric("投资方法", "科学配置")
        st.markdown("""
        ✓ 现代投资组合理论
        ✓ 风险平价配置
        ✓ 定期再平衡
        ✓ 情绪化管理
        """)

    st.markdown("---")
    st.markdown("## 🎯 使用流程")

    st.markdown("""
    1. **风险评估** → 了解您的风险承受能力
    2. **资产配置** → 获得个性化配置方案
    3. **基金筛选** → 找到合适的投资标的
    4. **AI顾问** → 解答投资疑问
    5. **长期陪伴** → 持续优化调整
    """)

    st.success("👈 请从左侧导航栏开始您的投资之旅！")


def show_risk_assessment():
    """风险评估页面"""
    st.header("🔍 风险评估")

    st.markdown("""
    通过以下问题，我们将为您评估风险承受类型，
    并为您匹配适合的投资组合方案。
    """)

    with st.form("risk_assessment_form"):
        st.markdown("### 📋 基本信息")

        col1, col2 = st.columns(2)

        with col1:
            age = st.slider("您的年龄", 18, 80, 30)
            investment_experience = st.selectbox(
                "投资经验",
                ["无", "1-3年", "3年以上"]
            )

        with col2:
            risk_tolerance = st.selectbox(
                "风险偏好",
                ["保守", "平衡", "进取"]
            )
            investment_goal = st.selectbox(
                "投资目标",
                ["资产保值", "稳健增值", "快速增值"]
            )

        time_horizon = st.selectbox(
            "投资期限",
            ["1年以内", "1-3年", "3年以上"]
        )

        submitted = st.form_submit_button("📊 提交评估")

        if submitted:
            # 评估风险类型
            answers = {
                "age": age,
                "investment_experience": investment_experience,
                "risk_tolerance": risk_tolerance,
                "investment_goal": investment_goal,
                "time_horizon": time_horizon
            }

            risk_profile = advisor.assess_risk_profile(answers)

            # 显示结果
            st.success(f"✅ 您的风险类型是：**{advisor.risk_profiles[risk_profile]['name']}**")
            st.info(f"💡 {advisor.risk_profiles[risk_profile]['description']}")

            # 保存到session
            st.session_state['risk_profile'] = risk_profile
            st.session_state['user_answers'] = answers

            # 显示建议
            st.markdown("### 📈 投资建议")

            if risk_profile == "conservative":
                st.markdown("""
                - 以债券和货币基金为主
                - 适当配置宽基指数
                - 避免高风险品种
                """)
            elif risk_profile == "balanced":
                st.markdown("""
                - 股债平衡配置
                - 核心以宽基指数为主
                - 适当配置行业主题
                """)
            else:
                st.markdown("""
                - 以权益类资产为主
                - 核心配置宽基指数
                - 卫星配置高成长主题
                - 可承受较大波动
                """)


def show_portfolio_allocation():
    """资产配置页面"""
    st.header("💼 资产配置建议")

    # 检查是否已做风险评估
    if 'risk_profile' not in st.session_state:
        st.warning("⚠️ 请先完成风险评估")
        st.info("👈 请前往「风险评估」页面")
        return

    risk_profile = st.session_state['risk_profile']

    # 投资金额输入
    invest_amount = st.number_input(
        "投资金额（元）",
        min_value=10000,
        max_value=10000000,
        value=100000,
        step=10000
    )

    # 生成配置方案
    portfolio = advisor.generate_portfolio(risk_profile, invest_amount)

    # 显示配置结果
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### {portfolio['risk_profile']}投资组合")

        # 核心-卫星饼图
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('核心配置', '卫星配置'),
            specs=[[{'type': 'pie'}, {'type': 'pie'}]]
        )

        # 核心配置
        core_labels = [item['category'] for item in portfolio['core_allocation']]
        core_values = [item['amount'] for item in portfolio['core_allocation']]

        fig.add_trace(
            go.Pie(
                labels=core_labels,
                values=core_values,
                hole=0.3
            ),
            row=1, col=1
        )

        # 卫星配置
        satellite_labels = [item['category'] for item in portfolio['satellite_allocation']]
        satellite_values = [item['amount'] for item in portfolio['satellite_allocation']]

        fig.add_trace(
            go.Pie(
                labels=satellite_labels,
                values=satellite_values,
                hole=0.3
            ),
            row=1, col=2
        )

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 配置详情")

        st.metric("预期年化收益", portfolio['expected_return'])
        st.metric("预期波动率", portfolio['expected_volatility'])
        st.metric("核心:卫星", portfolio['core_satellite_ratio'])

        st.markdown("---")

        st.markdown("**核心配置**")
        for item in portfolio['core_allocation']:
            st.markdown(f"- **{item['category']}**: {item['ratio']*100}%")

        st.markdown("**卫星配置**")
        for item in portfolio['satellite_allocation']:
            st.markdown(f"- **{item['category']}**: {item['ratio']*100}%")

    # 详细说明
    st.markdown("---")
    st.markdown("### 📝 配置说明")

    st.markdown("**核心配置**（追求稳健收益）")
    for item in portfolio['core_allocation']:
        with st.expander(f"📌 {item['category']} - {item['ratio']*100}%"):
            st.markdown(f"**投资理由**: {item['rationale']}")
            st.markdown(f"**示例标的**: {', '.join(item['examples'])}")
            st.markdown(f"**配置金额**: ¥{item['amount']:,.2f}")

    st.markdown("**卫星配置**（追求超额收益）")
    for item in portfolio['satellite_allocation']:
        with st.expander(f"🎯 {item['category']} - {item['ratio']*100}%"):
            st.markdown(f"**投资理由**: {item['rationale']}")
            st.markdown(f"**风险等级**: {item['risk']}")
            st.markdown(f"**配置金额**: ¥{item['amount']:,.2f}")

    # AI解释
    if st.button("🤖 AI解释配置方案"):
        with st.spinner("AI正在分析..."):
            explanation = ai_assistant.explain_portfolio(portfolio)
            st.info(explanation)


def show_fund_selection():
    """基金筛选页面"""
    st.header("📊 基金筛选")

    # 搜索功能
    col1, col2 = st.columns([3, 1])

    with col1:
        keyword = st.text_input("🔍 搜索基金名称或代码")

    with col2:
        search_button = st.button("搜索")

    # 推荐基金
    st.markdown("---")
    st.markdown("### ⭐ 推荐基金")

    recommended_funds = fund_query.get_recommended_funds()

    for fund in recommended_funds:
        with st.expander(f"📈 {fund['name']} ({fund['code']})"):
            col1, col2, col3 = st.columns(3)

            col1.metric("类型", fund['type'])
            col2.metric("风险", fund['risk'])
            col3.metric("分类", fund['category'])

            if st.button(f"查看详情", key=fund['code']):
                # 获取基金业绩
                performance = fund_query.get_fund_performance(fund['code'])

                if performance:
                    st.markdown("**业绩表现**")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("最新净值", performance.get('latest_nav', 'N/A'))
                    col2.metric("累计收益率", f"{performance.get('total_return', 'N/A')}%")
                    col3.metric("最大回撤", f"{performance.get('max_drawdown', 'N/A')}%")

    # 搜索结果
    if keyword and search_button:
        st.markdown("---")
        st.markdown(f"### 🔍 搜索结果: {keyword}")

        with st.spinner("搜索中..."):
            results = fund_query.search_fund_by_name(keyword)

        if not results.empty:
            st.dataframe(
                results.head(10),
                use_container_width=True
            )
        else:
            st.warning("未找到相关基金")


def show_ai_advisor():
    """AI顾问页面"""
    st.header("🤖 AI智能顾问")

    st.markdown("""
    您可以向我咨询任何投资相关问题，我会基于买方投顾理念为您提供建议。
    """)

    # 初始化聊天历史
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # 用户输入
    if prompt := st.chat_input("请输入您的问题..."):

        # 显示用户消息
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # 获取用户画像（如果存在）
        context = None
        if 'risk_profile' in st.session_state:
            context = f"风险类型: {advisor.risk_profiles[st.session_state['risk_profile']]['name']}"

        # AI回复
        with st.chat_message('assistant'):
            with st.spinner("思考中..."):
                response = ai_assistant.chat(prompt, context)
                st.markdown(response)

        st.session_state.messages.append({'role': 'assistant', 'content': response})

    # 常见问题
    st.markdown("---")
    st.markdown("### 💡 常见问题")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("什么是核心-卫星策略？"):
            st.session_state.messages.append({
                'role': 'user',
                'content': '什么是核心-卫星策略？'
            })

        if st.button("新手应该怎么开始投资？"):
            st.session_state.messages.append({
                'role': 'user',
                'content': '新手应该怎么开始投资？'
            })

    with col2:
        if st.button("如何降低投资风险？"):
            st.session_state.messages.append({
                'role': 'user',
                'content': '如何降低投资风险？'
            })

        if st.button("什么是资产配置？"):
            st.session_state.messages.append({
                'role': 'user',
                'content': '什么是资产配置？'
            })


def show_investment_knowledge():
    """投资知识页面"""
    st.header("📚 投资知识库")

    st.markdown("""
    以下是我们为您整理的投资基础知识，帮助您更好地理解投资。
    """)

    # 知识分类
    topics = [
        {
            "title": "📖 核心概念",
            "content": """
            **现代投资组合理论（MPT）**
            - 由马科维茨提出，强调通过资产配置降低风险
            - 核心思想：不要把鸡蛋放在同一个篮子里
            - 诺贝尔经济学奖获奖理论

            **核心-卫星策略**
            - 核心（75%）：追求市场平均收益
            - 卫星（25%）：追求超额收益
            - 平衡稳健与机会

            **夏普比率**
            - 衡量风险调整后收益的指标
            - 数值越高，单位风险的收益越高
            - 选择基金时的重要参考
            """
        },
        {
            "title": "⚖️ 风险管理",
            "content": """
            **最大回撤**
            - 从历史最高点到最低点的跌幅
            - 衡量最坏情况下的损失
            - 建议控制在20%以内

            **波动率**
            - 收益率的标准差
            - 衡量价格波动的剧烈程度
            - 波动率越高，风险越大

            **相关性**
            - 不同资产价格变动的关联程度
            - 相关性越低，分散风险效果越好
            - 股债相关性通常为负
            """
        },
        {
            "title": "🎯 投资原则",
            "content": """
            **长期投资**
            - 基金投资适合3年以上持有
            - 时间可以平滑短期波动
            - 复利效应需要时间积累

            **定投策略**
            - 定期定额买入
            - 降低择时风险
            - 适合工薪阶层

            **再平衡**
            - 定期调整配置比例
            - 维持目标风险水平
            - 高卖低买，提高收益

            **投资者适当性**
            - 只投资适合自己风险承受能力的产品
            - 不要追求超出能力范围的收益
            - 理解才能投资
            """
        },
        {
            "title": "📊 基金类型",
            "content": """
            **指数基金**
            - 跟踪特定指数
            - 费用低廉
            - 适合核心配置

            **主动管理基金**
            - 基金经理主动选股
            - 追求超额收益
            - 费用较高

            **债券基金**
            - 主要投资债券
            - 风险较低
            - 收益相对稳定

            **QDII基金**
            - 投资海外市场
            - 分散单一市场风险
            - 汇率风险需要考虑
            """
        }
    ]

    for topic in topics:
        with st.expander(topic['title']):
            st.markdown(topic['content'])


if __name__ == "__main__":
    main()
