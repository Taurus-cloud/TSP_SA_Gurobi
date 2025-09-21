import numpy as np
import time


class TspSA:
    def __init__(self, dist_matrix, coordinates):
        self.dist_matrix = dist_matrix
        self.coordinates = coordinates
        self.n = coordinates.shape[0]
        self.tour = None
        self.distance = None
        self.solve_time = None

    def solve(self, a=0.99, t0=97, tf=3, markov_length=10000):
        """使用模拟退火算法求解TSP问题"""
        start_time = time.time()

        n = self.n
        sol_new = np.arange(n)
        np.random.shuffle(sol_new)

        sol_current = sol_new.copy()
        sol_best = sol_new.copy()

        def calculate_distance(solution):
            total_dist = 0
            for i in range(n - 1):
                total_dist += self.dist_matrix[solution[i], solution[i + 1]]
            total_dist += self.dist_matrix[solution[-1], solution[0]]
            return total_dist

        E_current = calculate_distance(sol_current)
        E_best = E_current
        E_new = E_current

        t = t0
        while t >= tf:
            for _ in range(markov_length):
                # 产生新解
                if np.random.rand() < 0.5:
                    # 两交换
                    ind1, ind2 = np.random.choice(n, 2, replace=False)
                    sol_new[ind1], sol_new[ind2] = sol_new[ind2], sol_new[ind1]
                else:
                    # 三交换
                    ind1, ind2, ind3 = np.random.choice(n, 3, replace=False)
                    indices = sorted([ind1, ind2, ind3])
                    ind1, ind2, ind3 = indices

                    # 执行三交换操作
                    sol_new = np.concatenate([
                        sol_new[:ind1 + 1],
                        sol_new[ind2:ind3 + 1],
                        sol_new[ind1 + 1:ind2],
                        sol_new[ind3 + 1:]
                    ])

                E_new = calculate_distance(sol_new)

                # 接受准则
                if E_new < E_current:
                    E_current = E_new
                    sol_current = sol_new.copy()
                    if E_new < E_best:
                        E_best = E_new
                        sol_best = sol_new.copy()
                else:
                    if np.random.rand() < np.exp(-(E_new - E_current) / t):
                        E_current = E_new
                        sol_current = sol_new.copy()
                    else:
                        sol_new = sol_current.copy()

            t *= a

        end_time = time.time()
        self.solve_time = end_time - start_time
        self.tour = sol_best
        self.distance = E_best

        return True

    def get_results(self):
        """获取求解结果"""
        return {
            'tour': self.tour,
            'distance': self.distance,
            'solve_time': self.solve_time
        }

    def print_results(self):
        """打印求解结果"""
        if self.tour is not None:
            print("模拟退火求解结果:")
            print(f"最优路径: {[city + 1 for city in self.tour]}")
            print(f"路径长度: {self.distance}")
            print(f"求解时间: {self.solve_time:.2f}秒")
        else:
            print("模拟退火未能找到可行解")