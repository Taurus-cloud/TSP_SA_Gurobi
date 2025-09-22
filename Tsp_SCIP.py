from pyscipopt import Model, quicksum, multidict
import time
import numpy as np


class TspScip:
    def __init__(self, dist_matrix, n_cities):
        self.dist_matrix = dist_matrix
        self.n = n_cities
        self.tour = None
        self.distance = None
        self.solve_time = None
        self.obj_val = None
        self.mip_gap = None

    def solve(self, time_limit=1800, mip_gap=0.0001, presolve=True, cuts=True, heuristics=True, output_flag=False):
        """使用SCIP求解TSP问题"""
        start_time = time.time()

        # 创建模型
        model = Model("TSP")

        # 设置参数
        model.setParam("limits/time", time_limit)  # 时间限制（秒）
        model.setParam("limits/gap", mip_gap)  # MIP间隙
        model.setParam("presolving/maxrounds", 2 if presolve else 0)  # 预求解
        model.setParam("separating/maxrounds", 3 if cuts else 0)  # 割平面
        model.setParam("heuristics/rounding/freq", 10 if heuristics else -1)  # 启发式
        model.hideOutput(not output_flag)  # 控制输出

        # 创建变量
        x = {}
        u = {}

        for i in range(self.n):
            u[i] = model.addVar(f"u_{i}", vtype="C", lb=0, ub=self.n - 1)
            for j in range(self.n):
                if i != j:
                    x[i, j] = model.addVar(f"x_{i}_{j}", vtype="B")

        # 设置目标函数
        objective = quicksum(self.dist_matrix[i, j] * x[i, j]
                             for i in range(self.n) for j in range(self.n) if i != j)
        model.setObjective(objective, "minimize")

        # 添加约束
        # 每个城市恰好有一条进入的边
        for j in range(self.n):
            model.addCons(quicksum(x[i, j] for i in range(self.n) if i != j) == 1,
                          f"in_flow_{j}")

        # 每个城市恰好有一条出去的边
        for i in range(self.n):
            model.addCons(quicksum(x[i, j] for j in range(self.n) if i != j) == 1,
                          f"out_flow_{i}")

        # 子回路消除约束 (MTZ约束)
        for i in range(1, self.n):
            for j in range(1, self.n):
                if i != j:
                    model.addCons(u[i] - u[j] + self.n * x[i, j] <= self.n - 1,
                                  f"subtour_elim_{i}_{j}")

        # 设置u[0] = 0
        model.addCons(u[0] == 0, "u0_fix")

        # 求解模型
        model.optimize()

        end_time = time.time()
        self.solve_time = end_time - start_time

        # 提取解
        if model.getStatus() == "optimal" or model.getStatus() == "timelimit":
            # 构建路径
            tour = [0]
            current_city = 0
            visited = set([0])

            while len(visited) < self.n:
                for j in range(self.n):
                    if j != current_city and model.getVal(x[current_city, j]) > 0.5:
                        tour.append(j)
                        visited.add(j)
                        current_city = j
                        break

            # 计算总距离
            total_distance = 0
            for i in range(self.n):
                total_distance += self.dist_matrix[tour[i], tour[(i + 1) % self.n]]

            self.tour = tour
            self.distance = total_distance
            self.obj_val = model.getObjVal()

            # 计算MIP间隙
            try:
                primal_bound = model.getPrimalbound()
                dual_bound = model.getDualbound()
                if abs(primal_bound) > 1e-6:
                    self.mip_gap = abs(primal_bound - dual_bound) / abs(primal_bound)
                else:
                    self.mip_gap = 0.0
            except:
                self.mip_gap = None

            return True
        else:
            return False

    def get_results(self):
        """获取求解结果"""
        return {
            'tour': self.tour,
            'distance': self.distance,
            'solve_time': self.solve_time,
            'obj_val': self.obj_val,
            'mip_gap': self.mip_gap
        }

    def print_results(self):
        """打印求解结果"""
        if self.tour is not None:
            print("SCIP求解结果:")
            print(f"最优路径: {[city + 1 for city in self.tour]}")
            print(f"路径长度: {self.distance}")
            print(f"求解时间: {self.solve_time:.2f}秒")
            print(f"目标函数值: {self.obj_val}")
            print(f"MIP间隙: {self.mip_gap}")
        else:
            print("SCIP未能找到可行解")