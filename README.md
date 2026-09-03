# 2024 高教社杯数学建模 B题：生产过程中的决策问题

本仓库是 2024 年高教社杯全国大学生数学建模竞赛 B 题的学习与建模实现，包含官方参数整理、四问模型、可复现代码、测试、计算结果及论文用图表。

## 主要内容

- `2024B题原题.md`：题目结构和官方参数表整理。
- `reports/ANALYSIS_MODELING_REPORT.md`：问题拆解、假设、公式和求解方法。
- `reports/RESULTS_REPORT.md`：计算结果、约束检查和复现说明。
- `reports/BEGINNER_GUIDE.md`：面向数学建模新手的学习路线。
- `code/`：问题一至四、灵敏度分析和自动化测试。
- `results/`：程序生成的标准 JSON 结果。
- `figures/`：程序生成的 PDF 矢量图。

## 建模路线

1. 问题一：精确二项分布与单侧假设检验。
2. 问题二：两零配件生产决策的 16 种组合枚举。
3. 问题三：8 个零件、3 个半成品、1 个成品的 16 维决策枚举。
4. 问题四：Beta 后验分布与全次品率不确定性传播。

模型采用“安全回流约束”：拆解并复用下级投入品时，必须执行相应检测，以避免未检坏件无限循环。问题一使用 8%/12% 工程判别带；这两项均为显式建模假设，并非题面直接给定。

## 运行

```powershell
python code/problem1.py
python code/problem2.py
python code/problem3.py
python code/problem4.py
python code/sensitivity.py
```

运行测试：

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest code/tests -q
```

## 数据来源

题目与参数来自 [2024 年高教社杯 B 题赛题 PDF](https://www.shumo.com/wiki/lib/exe/fetch.php?media=cumcm:cumcm2024b.pdf)。正式引用和参赛提交请以原始 PDF 及当年竞赛规范为准。
