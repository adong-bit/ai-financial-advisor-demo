# 贡献指南

感谢您对AI智能投顾助手项目的关注！

## 如何贡献

### 报告问题

如果您发现了bug或有功能建议，请：

1. 检查 [Issues](https://github.com/adong-bit/ai-financial-advisor-demo/issues) 是否已有类似问题
2. 如果没有，创建新的Issue，详细描述：
   - 问题和复现步骤
   - 预期行为
   - 截图（如果适用）
   - 环境信息（操作系统、Python版本等）

### 提交代码

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

### 开发规范

- 代码风格：遵循PEP 8
- 提交信息：使用清晰的commit message
- 注释：关键逻辑需要添加中文注释
- 测试：新功能需要包含测试用例

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/adong-bit/ai-financial-advisor-demo.git

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

## 代码审查

所有Pull Request都需要通过代码审查才能合并。审查重点：
- 代码质量
- 功能正确性
- 文档完整性
- 测试覆盖

## 许可证

通过贡献代码，您同意您的贡献将使用MIT许可证授权。
