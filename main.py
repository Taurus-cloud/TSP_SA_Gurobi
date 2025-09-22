from data import TSPData
from Tsp_Gurobi import TspGurobi
from Tsp_SCIP import TspScip  # 新增SCIP求解器导入
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

    # 使用SCIP求解
    print("\n开始使用SCIP求解TSP问题...")
    scip_solver = TspScip(dist_matrix, n)
    scip_success = scip_solver.solve(
        time_limit=1800,
        mip_gap=0.0001,
        presolve=True,
        cuts=True,
        heuristics=True
    )
    scip_results = scip_solver.get_results()
    scip_solver.print_results()

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

    # 比较三种算法
    print("\n" + "=" * 50)
    print("算法比较:")
    print("=" * 50)

    # 创建结果表格
    results = []
    if gurobi_success:
        results.append(("Gurobi", gurobi_results['distance'], gurobi_results['solve_time'],
                        gurobi_results['obj_val'], gurobi_results.get('mip_gap', 'N/A')))

    if scip_success:
        results.append(("SCIP", scip_results['distance'], scip_results['solve_time'],
                        scip_results['obj_val'], scip_results.get('mip_gap', 'N/A')))

    results.append(("模拟退火", sa_results['distance'], sa_results['solve_time'],
                    sa_results['distance'], 'N/A'))  # 模拟退火没有MIP间隙

    # 打印比较结果
    print(f"{'算法':<10} {'路径长度':<12} {'求解时间(秒)':<15} {'目标函数值':<15} {'MIP间隙':<10}")
    print("-" * 70)
    for name, distance, time, obj_val, gap in results:
        print(f"{name:<10} {distance:<12.2f} {time:<15.2f} {obj_val:<15.2f} {gap:<10}")

    # 找出最优解
    if gurobi_success or scip_success:
        valid_results = [(name, dist) for name, dist, _, _, _ in results if
                         name != "模拟退火" or (name == "模拟退火" and dist > 0)]
        if valid_results:
            best_algorithm = min(valid_results, key=lambda x: x[1])
            print(f"\n最优算法: {best_algorithm[0]}, 路径长度: {best_algorithm[1]:.2f}")

    # 计算相对差距
    if gurobi_success and scip_success:
        gap_gurobi_scip = abs(gurobi_results['distance'] - scip_results['distance']) / min(gurobi_results['distance'],
                                                                                           scip_results[
                                                                                               'distance']) * 100
        print(f"Gurobi与SCIP相对差距: {gap_gurobi_scip:.2f}%")

    if gurobi_success:
        gap_gurobi_sa = abs(gurobi_results['distance'] - sa_results['distance']) / gurobi_results['distance'] * 100
        print(f"Gurobi与模拟退火相对差距: {gap_gurobi_sa:.2f}%")

    if scip_success:
        gap_scip_sa = abs(scip_results['distance'] - sa_results['distance']) / scip_results['distance'] * 100
        print(f"SCIP与模拟退火相对差距: {gap_scip_sa:.2f}%")

    # 可视化结果
    visualizer = TSPVisualizer(coordinates)

    # 使用扩展后的plot_comparison函数进行可视化
    if gurobi_success and scip_success:
        # 三种算法都有结果
        visualizer.plot_comparison(
            sa_results['tour'],
            sa_results['distance'],
            gurobi_results['tour'],
            gurobi_results['distance'],
            scip_results['tour'],
            scip_results['distance']
        )
    elif gurobi_success:
        # 只有Gurobi和模拟退火有结果
        visualizer.plot_comparison(
            sa_results['tour'],
            sa_results['distance'],
            gurobi_results['tour'],
            gurobi_results['distance']
        )
    elif scip_success:
        # 只有SCIP和模拟退火有结果
        visualizer.plot_comparison(
            sa_results['tour'],
            sa_results['distance'],
            scip_results['tour'],
            scip_results['distance']
        )
    else:
        # 只有模拟退火有结果
        visualizer.plot_comparison(
            sa_results['tour'],
            sa_results['distance'],
            None,
            None
        )

    # 使用新的多算法比较函数
    tours = []
    distances = []
    labels = []

    if gurobi_success:
        tours.append(gurobi_results['tour'])
        distances.append(gurobi_results['distance'])
        labels.append("Gurobi")

    if scip_success:
        tours.append(scip_results['tour'])
        distances.append(scip_results['distance'])
        labels.append("SCIP")

    tours.append(sa_results['tour'])
    distances.append(sa_results['distance'])
    labels.append("模拟退火")

    visualizer.plot_multiple_comparison(tours, distances, labels)


if __name__ == "__main__":
    main()