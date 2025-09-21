# TSP求解器比较项目

一个用于比较不同算法解决旅行商问题（TSP）性能的Python项目。本项目实现了两种TSP求解算法：使用Gurobi的精确求解方法和模拟退火启发式算法，并提供了可视化比较功能。

## 项目结构

```
tsp_project/
│
├── data.py              # 数据加载和处理类
├── Tsp_Gurobi.py        # Gurobi求解器类
├── Tsp_SA.py           # 模拟退火求解器类
├── visual.py           # 可视化功能类
├── main.py             # 主程序
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明文档
```

## 功能特点

- **多算法比较**：支持Gurobi精确求解和模拟退火启发式算法
- **可视化展示**：提供两种算法求解结果的直观比较
- **参数可配置**：两种算法的参数均可灵活调整
- **性能评估**：自动比较求解时间和解的质量
- **模块化设计**：代码结构清晰，易于扩展和维护

## 安装依赖

在运行项目前，请确保安装以下依赖：

```bash
pip install numpy matplotlib gurobipy
```

注意：Gurobi需要额外的许可证。请访问[Gurobi官网](https://www.gurobi.com/)获取学术或商业许可证。

## 使用方法

### 1. 运行主程序

```bash
python main.py
```

### 2. 自定义数据

如需使用自定义城市坐标数据，可以修改`main.py`：

```python
# 加载自定义数据
custom_coordinates = [
    [x1, y1],
    [x2, y2],
    # ... 更多坐标
]
data_loader.load_custom_data(custom_coordinates)
```

### 3. 调整算法参数

在`main.py`中可以调整两种算法的参数：

```python
# 调整Gurobi参数
gurobi_success = gurobi_solver.solve(
    time_limit=1800,      # 求解时间限制（秒）
    mip_gap=0.0001,       # 最优间隙容忍度
    presolve=2,           # 预处理级别
    cuts=3,               # 切割生成级别
    heuristics=0.1,       # 启发式搜索比例
    output_flag=0         # 控制求解过程输出（0=关闭，1=开启）
)

# 调整模拟退火参数
sa_success = sa_solver.solve(
    a=0.99,               # 温度衰减系数
    t0=97,                # 初始温度
    tf=3,                 # 终止温度
    markov_length=10000   # Markov链长度
)
```

## 算法比较

本项目实现了两种TSP求解方法：

### 1. Gurobi精确求解
- 使用整数规划方法精确求解TSP问题
- 采用Miller-Tucker-Zemlin (MTZ)约束消除子回路
- 可配置求解精度和时间限制
- 适用于中小规模问题，能保证找到最优解

### 2. 模拟退火启发式算法
- 使用模拟退火 metaheuristic 方法
- 支持两交换和三交换邻域操作
- 求解速度快，适用于大规模问题
- 不能保证找到全局最优解，但通常能找到高质量解

## 输出结果

程序运行后将输出：
1. 两种算法的求解路径和长度
2. 求解时间比较
3. 解的质量比较
4. 可视化路径图

## 扩展功能

项目设计便于扩展，可以轻松添加：
1. 新的TSP求解算法（如遗传算法、蚁群算法等）
2. 不同的邻域操作和扰动策略
3. 批量测试和性能分析功能
4. 更多可视化选项

## 注意事项

1. Gurobi需要有效的许可证才能运行
2. 对于大规模TSP问题，Gurobi求解可能需要较长时间
3. 模拟退火算法的性能受参数设置影响较大
4. 项目默认使用48城市的标准TSP测试数据

## 许可证

本项目使用MIT许可证。请注意，Gurobi有其自己的许可协议，使用前请确保遵守相关条款。

## 贡献

欢迎提交Issue和Pull Request来改进本项目。

## 联系方式

如有问题或建议，请通过GitHub Issues提交反馈。