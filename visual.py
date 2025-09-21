import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['microsoft yahei']


class TSPVisualizer:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def plot_single_solution(self, tour, distance, title, ax=None):
        """绘制单个TSP解"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))

        # 绘制城市点
        ax.scatter(self.coordinates[:, 0], self.coordinates[:, 1], c='red', s=50, marker='o')

        # 绘制路径
        n = len(tour)
        for i in range(n - 1):
            city1 = tour[i]
            city2 = tour[i + 1]
            ax.plot([self.coordinates[city1, 0], self.coordinates[city2, 0]],
                    [self.coordinates[city1, 1], self.coordinates[city2, 1]], 'b-')

        # 绘制从最后一个城市回到第一个城市的路径
        ax.plot([self.coordinates[tour[-1], 0], self.coordinates[tour[0], 0]],
                [self.coordinates[tour[-1], 1], self.coordinates[tour[0], 1]], 'b-')

        ax.set_title(f'{title} (距离: {distance:.2f})')
        ax.set_xlabel('X坐标')
        ax.set_ylabel('Y坐标')
        ax.grid(True)

        if ax is None:
            plt.tight_layout()
            plt.show()

    def plot_comparison(self, sa_tour, sa_distance, gurobi_tour, gurobi_distance):
        """比较并绘制两种算法的解"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # 绘制模拟退火结果
        self.plot_single_solution(sa_tour, sa_distance, '模拟退火最优路径', ax1)

        # 绘制Gurobi结果
        if gurobi_tour is not None:
            self.plot_single_solution(gurobi_tour, gurobi_distance, 'Gurobi最优路径', ax2)
        else:
            ax2.text(0.5, 0.5, 'Gurobi未能找到可行解', ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title('Gurobi结果')

        plt.tight_layout()
        plt.show()