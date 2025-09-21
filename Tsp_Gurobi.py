import gurobipy as gp
from gurobipy import GRB
import time
import numpy as np


class TspGurobi:
    def __init__(self, dist_matrix, n_cities):
        self.dist_matrix = dist_matrix
        self.n = n_cities
        self.tour = None
        self.distance = None
        self.solve_time = None
        self.obj_val = None
        self.mip_gap = None

    def solve(self, time_limit=1800, mip_gap=0.0001, presolve=2, cuts=3, heuristics=0.1, output_flag=0):
        """使用Gurobi求解TSP问题"""
        start_time = time.time()

        # 创建模型
        model = gp.Model("TSP")

        # 创建变量
        x = model.addVars(self.n, self.n, vtype=GRB.BINARY, name="x")
        u = model.addVars(self.n, vtype=GRB.CONTINUOUS, name="u")

        # 设置目标函数
        obj = gp.quicksum(self.dist_matrix[i, j] * x[i, j] for i in range(self.n) for j in range(self.n) if i != j)
        model.setObjective(obj, GRB.MINIMIZE)

        # 添加约束
        model.addConstrs(gp.quicksum(x[i, j] for i in range(self.n) if i != j) == 1 for j in range(self.n))
        model.addConstrs(gp.quicksum(x[i, j] for j in range(self.n) if i != j) == 1 for i in range(self.n))

        # 子回路消除约束
        model.addConstrs(u[i] - u[j] + self.n * x[i, j] <= self.n - 1
                         for i in range(1, self.n) for j in range(1, self.n) if i != j)

        # 设置u变量的范围
        for i in range(1, self.n):
            model.addConstr(1 <= u[i])
            model.addConstr(u[i] <= self.n - 1)

        # 设置求解参数
        model.Params.OutputFlag = output_flag  # 控制求解过程输出
        model.Params.TimeLimit = time_limit
        model.Params.MIPGap = mip_gap
        model.Params.Presolve = presolve
        model.Params.Cuts = cuts
        model.Params.Heuristics = heuristics

        # 求解模型
        model.optimize()

        end_time = time.time()
        self.solve_time = end_time - start_time

        # 提取解
        if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
            # 构建路径
            tour = [0]
            current_city = 0
            visited = set([0])

            while len(visited) < self.n:
                for j in range(self.n):
                    if j != current_city and x[current_city, j].X > 0.5:
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
            self.obj_val = model.ObjVal
            self.mip_gap = model.MIPGap

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
            print("Gurobi求解结果:")
            print(f"最优路径: {[city + 1 for city in self.tour]}")
            print(f"路径长度: {self.distance}")
            print(f"求解时间: {self.solve_time:.2f}秒")
            print(f"目标函数值: {self.obj_val}")
            print(f"MIP间隙: {self.mip_gap}")
        else:
            print("Gurobi未能找到可行解")