from data import TSPData
from Tsp_Gurobi import TspGurobi
from Tsp_SA import TspSA
from visual import TSPVisualizer


def main():
    # 加载数据
    data_loader = TSPData()
    data_loader.load_default_data()
    coordinates, dist_matrix, n = data_loader.get_data()

    # 使用Gurobi求解
    print("开始使用Gurobi求解TSP问题...")
    gurobi_solver = TspGurobi(dist_matrix, n)
    gurobi_success = gurobi_solver.solve(
        time_limit=1800,
        mip_gap=0.0001,
        presolve=2,
        cuts=3,
        heuristics=0.1
    )
    gurobi_results = gurobi_solver.get_results()
    gurobi_solver.print_results()

    # 使用模拟退火求解
    print("\n开始使用模拟退火求解TSP问题...")
    sa_solver = TspSA(dist_matrix, coordinates)
    sa_success = sa_solver.solve(
        a=0.99,
        t0=97,
        tf=3,
        markov_length=10000
    )
    sa_results = sa_solver.get_results()
    sa_solver.print_results()

    # 比较两种算法
    print("\n算法比较:")
    if gurobi_success:
        print(f"Gurobi 路径长度: {gurobi_results['distance']}")
    else:
        print("Gurobi 未能找到可行解")

    print(f"模拟退火路径长度: {sa_results['distance']}")

    if gurobi_success:
        diff = abs(gurobi_results['distance'] - sa_results['distance'])
        print(f"路径长度差异: {diff:.2f}")
        if gurobi_results['distance'] < sa_results['distance']:
            print("Gurobi 解更优")
        elif gurobi_results['distance'] > sa_results['distance']:
            print("模拟退火解更优")
        else:
            print("两种算法解相同")

    print(f"Gurobi 求解时间: {gurobi_results['solve_time']:.2f}秒")
    print(f"模拟退火求解时间: {sa_results['solve_time']:.2f}秒")

    # 可视化结果
    visualizer = TSPVisualizer(coordinates)
    if gurobi_success:
        visualizer.plot_comparison(
            sa_results['tour'],
            sa_results['distance'],
            gurobi_results['tour'],
            gurobi_results['distance']
        )
    else:
        visualizer.plot_comparison(
            sa_results['tour'],
            sa_results['distance'],
            None,
            None
        )


if __name__ == "__main__":
    main()