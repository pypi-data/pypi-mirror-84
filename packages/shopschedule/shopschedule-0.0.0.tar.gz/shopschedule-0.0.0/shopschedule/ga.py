import logging
import time

import numpy as np

from . import Jsp, FJsp, Fsp, HFsp, Utils, deepcopy, plt
from .name import DataName, GaName

Utils.make_dir("log")
logging.basicConfig(filename='./log/ga.log', level=logging.INFO)


class Ga:
    """
    遗传算法
    """

    def __init__(self, pop_size, rate_crossover, rate_mutation, operator_crossover, operator_mutation,
                 operator_selection, stop_max_generation, stop_max_stay, function_objective, ):
        self.pop_size = pop_size
        self.rate_crossover = rate_crossover
        self.rate_mutation = rate_mutation
        self.operator_crossover = operator_crossover
        self.operator_mutation = operator_mutation
        self.operator_selection = operator_selection
        self.stop_max_generation = stop_max_generation
        self.stop_max_stay = stop_max_stay
        self.function_objective = function_objective
        # 定义
        self.pop_info = []
        self.pop_objective = np.zeros([self.pop_size, 1])
        self.pop_fitness = np.zeros([self.pop_size, 1])

        self.generation_objective = np.zeros([self.stop_max_generation + 1, 3])  # 最优、最差、平均
        self.generation_runtime = np.zeros([self.stop_max_generation + 1, 3])  # 开始、结束、计时

        self.global_best_info = None
        self.global_best_osc = None
        self.global_best_mac = None
        self.global_best_obj = None
        self.global_best_fitness = None

    # 【选择操作】轮盘赌选
    def selection_roulette(self, ):
        a = self.pop_fitness / sum(self.pop_fitness[:, 0])
        b = np.zeros([self.pop_size, 1])
        for i in range(self.pop_size):  # 计算个体的被选择概率
            b[i, 0] = sum(a[:i + 1])
        return b

    # 更新
    def update_generation(self, i, ):
        index_min = int(np.argmin(self.pop_objective[:, 0]))
        index_max = int(np.argmax(self.pop_objective[:, 0]))
        self.generation_objective[i, 0] = self.pop_objective[index_min]
        self.generation_objective[i, 1] = self.pop_objective[index_max]
        self.generation_objective[i, 2] = np.mean(self.pop_objective[:, 0])
        self.generation_runtime[i, 2] = self.generation_runtime[i, 1] - self.generation_runtime[i, 0]
        if self.global_best_info is None or Utils.update_info(self.global_best_obj, self.generation_objective[i, 0]):
            self.global_best_info = self.pop_info[index_min]
            self.global_best_osc = self.pop_info[index_min].osc
            self.global_best_mac = self.pop_info[index_min].mac
            self.global_best_obj = self.pop_objective[index_min][0]
            self.global_best_fitness = self.pop_fitness[index_min][0]
        # 记录
        msg = "Generation{:>3}:Runtime:{:<.2f},Best:{:<.2f},Worst:{:<.2f},Mean:{:<.2f}".format(
            i,
            self.generation_runtime[i, 2],
            self.global_best_obj,  # 不等于generation_objective[i, 0]
            self.generation_objective[i, 1],
            self.generation_objective[i, 2],
        )
        logging.info(msg)
        Utils.print(msg)

    def objective_png(self, file_name="ObjectiveTrace", dpi=200, ):
        plt.figure(figsize=[9, 5])
        plt.margins()
        plt.tight_layout()
        marker = ["v", "^", "o"]
        line = ['--', '-.', ':']
        label = ["Best", "Worst", "Mean"]
        for i in range(self.generation_objective.shape[1]):
            plt.plot(self.generation_objective[:, i], marker=marker[i], linestyle=line[i], label=label[i])
        plt.legend()
        Utils.figure_png(file_name=file_name, dpi=dpi)

    def runtime_png(self, file_name="Runtime", dpi=200, ):
        plt.figure(figsize=[9, 5])
        plt.margins()
        plt.tight_layout()
        plt.plot(self.generation_runtime[:, 2], marker="o", linestyle="--", label="Runtime")
        plt.legend()
        Utils.figure_png(file_name=file_name, dpi=dpi)


class GaJsp(Ga, Jsp):
    """
    作业车间调度的遗传算法
    """

    def __init__(self, para, data, ):
        pop_size = para[GaName.pop_size]
        rate_crossover = para[GaName.rate_crossover]
        rate_mutation = para[GaName.rate_mutation]
        operator_crossover = para[GaName.operator_crossover]
        operator_mutation = para[GaName.operator_mutation]
        operator_selection = para[GaName.operator_selection]
        stop_max_generation = para[GaName.stop_max_generation]
        stop_max_stay = para[GaName.stop_max_stay]
        function_objective = para[GaName.function_objective]
        Ga.__init__(self, pop_size, rate_crossover, rate_mutation, operator_crossover, operator_mutation,
                    operator_selection, stop_max_generation, stop_max_stay, function_objective, )
        Jsp.__init__(self, data[DataName.n], data[DataName.m],
                     data[DataName.ops], data[DataName.prt], )
        # 定义
        self.pop_osc = np.zeros([self.pop_size, self.length], dtype=int)

    def update_info(self, i, obj_new, info_new, osc_new, ):
        if Utils.update_info(self.pop_objective[i], obj_new):
            self.pop_info[i] = info_new
            self.pop_osc[i] = osc_new
            self.pop_objective[i] = obj_new
            self.pop_fitness[i] = Utils.calculate_fitness(obj_new)

    def do_init(self, ):
        self.generation_runtime[0, 0] = time.perf_counter()
        for i in range(self.pop_size):
            self.pop_osc[i] = self.code_osc_jsp()
            info = self.decode_jsp(self.pop_osc[i])
            self.pop_info.append(info)
            self.pop_objective[i] = self.function_objective(info)
            self.pop_fitness[i] = Utils.calculate_fitness(self.pop_objective[i])
        self.generation_runtime[0, 1] = time.perf_counter()
        self.update_generation(0)

    def do_selection_roulette(self, ):
        a = self.selection_roulette()
        pop_osc = deepcopy(self.pop_osc)
        pop_objective = deepcopy(self.pop_objective)
        pop_fitness = deepcopy(self.pop_fitness)
        pop_info = deepcopy(self.pop_info)
        for i in range(self.pop_size):
            j = np.argwhere(a[:, 0] > np.random.random())[0, 0]
            self.pop_osc[i] = pop_osc[j]
            self.pop_objective[i] = pop_objective[j]
            self.pop_fitness[i] = pop_fitness[j]
            self.pop_info[i] = pop_info[j]
        index = int(np.argmax(self.pop_fitness[:, 0]))
        self.pop_info[index] = self.global_best_info
        self.pop_osc[index] = self.global_best_osc
        self.pop_objective[index] = self.global_best_obj
        self.pop_fitness[index] = self.global_best_fitness

    def do_crossover_pox(self, i, j, ):
        osc1, osc2 = self.pop_info[i].crossover_pox_osc(self.pop_info[j])
        info1 = self.decode_jsp(osc1)
        obj1 = self.function_objective(info1)
        self.update_info(i, obj1, info1, osc1)
        info2 = self.decode_jsp(osc2)
        obj2 = self.function_objective(info2)
        self.update_info(j, obj2, info2, osc2)

    def do_mutation_tpe(self, i, ):
        osc1 = self.pop_info[i].mutation_tpe_osc()
        info1 = self.decode_jsp(osc1)
        obj1 = self.function_objective(info1)
        self.update_info(i, obj1, info1, osc1)

    def start_generation(self, ):
        self.do_init()
        for g in range(1, self.stop_max_generation + 1):
            self.generation_runtime[g, 0] = time.perf_counter()
            for i in range(self.pop_size):
                if np.random.random() < self.rate_crossover:
                    j = np.random.choice(np.delete(np.arange(self.pop_size), i), 1, replace=False)[0]
                    self.do_crossover_pox(i, j)
                if np.random.random() < self.rate_mutation:
                    self.do_mutation_tpe(i)
            self.do_selection_roulette()
            self.generation_runtime[g, 1] = time.perf_counter()
            self.update_generation(g)
            if g >= self.stop_max_stay and np.std(self.generation_objective[g - self.stop_max_stay + 1:g + 1, 0]) == 0:
                k = np.arange(g + 1, self.stop_max_generation + 1)
                self.generation_objective = np.delete(self.generation_objective, k, axis=0)
                self.generation_runtime = np.delete(self.generation_runtime, k, axis=0)
                break
        self.global_best_info.std_code()
        self.global_best_osc = self.global_best_info.osc
        for i in range(self.pop_size):
            self.pop_info[i].std_code()
            self.pop_osc[i] = self.pop_info[i].osc


class GaFJsp(Ga, FJsp):
    """
    柔性作业车间调度的遗传算法
    """

    def __init__(self, para, data, method, ):
        pop_size = para[GaName.pop_size]
        rate_crossover = para[GaName.rate_crossover]
        rate_mutation = para[GaName.rate_mutation]
        operator_crossover = para[GaName.operator_crossover]
        operator_mutation = para[GaName.operator_mutation]
        operator_selection = para[GaName.operator_selection]
        stop_max_generation = para[GaName.stop_max_generation]
        stop_max_stay = para[GaName.stop_max_stay]
        function_objective = para[GaName.function_objective]
        Ga.__init__(self, pop_size, rate_crossover, rate_mutation, operator_crossover, operator_mutation,
                    operator_selection, stop_max_generation, stop_max_stay, function_objective, )
        FJsp.__init__(self, data[DataName.n], data[DataName.m],
                      data[DataName.p_list], data[DataName.ops_list], data[DataName.prt_list], )
        self.method = method
        # 定义
        self.pop_osc = np.zeros([self.pop_size, self.length], dtype=int)
        self.pop_mac = []
        for i in range(self.pop_size):
            self.pop_mac.append([])

    def update_info_osc(self, i, obj_new, info_new, osc_new, ):
        if Utils.update_info(self.pop_objective[i], obj_new):
            self.pop_info[i] = info_new
            self.pop_osc[i] = osc_new
            if self.method == "3":
                self.pop_mac[i] = info_new.mac_info
            self.pop_objective[i] = obj_new
            self.pop_fitness[i] = Utils.calculate_fitness(obj_new)

    def update_info_mac(self, i, obj_new, info_new, mac_new, ):
        if Utils.update_info(self.pop_objective[i], obj_new):
            self.pop_info[i] = info_new
            self.pop_mac[i] = mac_new
            self.pop_objective[i] = obj_new
            self.pop_fitness[i] = Utils.calculate_fitness(obj_new)

    def decode_fjsp_method(self, osc, mac=None, ):
        return self.decode_fjsp(osc, mac, self.method)

    def do_init(self, ):
        self.generation_runtime[0, 0] = time.perf_counter()
        for i in range(self.pop_size):
            self.pop_osc[i] = self.code_osc_fjsp()
            if self.method in ["1", "2", ]:
                if self.method == "1":
                    self.pop_mac[i] = self.code_mac1_fjsp(self.pop_osc[i])
                else:
                    self.pop_mac[i] = self.code_mac2_fjsp()
                info = self.decode_fjsp_method(self.pop_osc[i], self.pop_mac[i])
            else:
                info = self.decode_fjsp_method(self.pop_osc[i])
                self.pop_mac[i] = info.mac
            self.pop_info.append(info)
            self.pop_objective[i] = self.function_objective(info)
            self.pop_fitness[i] = Utils.calculate_fitness(self.pop_objective[i])
        self.generation_runtime[0, 1] = time.perf_counter()
        self.update_generation(0)

    def do_selection_roulette(self, ):
        a = self.selection_roulette()
        pop_osc = deepcopy(self.pop_osc)
        pop_mac = deepcopy(self.pop_mac)
        pop_objective = deepcopy(self.pop_objective)
        pop_fitness = deepcopy(self.pop_fitness)
        pop_info = deepcopy(self.pop_info)
        for i in range(self.pop_size):
            j = np.argwhere(a[:, 0] > np.random.random())[0, 0]
            self.pop_osc[i] = pop_osc[j]
            self.pop_mac[i] = pop_mac[j]
            self.pop_objective[i] = pop_objective[j]
            self.pop_fitness[i] = pop_fitness[j]
            self.pop_info[i] = pop_info[j]
        index = int(np.argmax(self.pop_fitness[:, 0]))
        self.pop_info[index] = self.global_best_info
        self.pop_osc[index] = self.global_best_osc
        self.pop_mac[index] = self.global_best_mac
        self.pop_objective[index] = self.global_best_obj
        self.pop_fitness[index] = self.global_best_fitness

    def do_crossover_osc_ipox(self, i, j, ):
        osc1, osc2 = self.pop_info[i].crossover_ipox_osc(self.pop_info[j])
        info1 = self.decode_fjsp_method(osc1, self.pop_mac[i])
        obj1 = self.function_objective(info1)
        self.update_info_osc(i, obj1, info1, osc1)
        info2 = self.decode_fjsp_method(osc2, self.pop_mac[j])
        obj2 = self.function_objective(info2)
        self.update_info_osc(j, obj2, info2, osc2)

    def do_mutation_osc_tpe(self, i, ):
        osc1 = self.pop_info[i].mutation_tpe_osc()
        info1 = self.decode_fjsp_method(osc1, self.pop_mac[i])
        obj1 = self.function_objective(info1)
        self.update_info_osc(i, obj1, info1, osc1)

    def do_crossover_mac_random(self, i, j, ):
        mac1, mac2 = self.pop_info[i].crossover_random_mac2(self.pop_info[j])
        info1 = self.decode_fjsp_method(self.pop_osc[i], mac1)
        obj1 = self.function_objective(info1)
        self.update_info_mac(i, obj1, info1, mac1)
        info2 = self.decode_fjsp_method(self.pop_osc[j], mac2)
        obj2 = self.function_objective(info2)
        self.update_info_mac(i, obj2, info2, mac2)

    def do_mutation_mac_replace(self, i, ):
        mac1 = self.pop_info[i].mutation_replace_mac2()
        info1 = self.decode_fjsp_method(self.pop_osc[i], mac1)
        obj1 = self.function_objective(info1)
        self.update_info_mac(i, obj1, info1, mac1)

    def start_generation(self, ):
        self.do_init()
        for g in range(1, self.stop_max_generation + 1):
            self.generation_runtime[g, 0] = time.perf_counter()
            for i in range(self.pop_size):
                if np.random.random() < self.rate_crossover:
                    j = np.random.choice(np.delete(np.arange(self.pop_size), i), 1, replace=False)[0]
                    self.do_crossover_osc_ipox(i, j)
                    if self.method == "2":
                        self.do_crossover_mac_random(i, j)
                if np.random.random() < self.rate_mutation:
                    self.do_mutation_osc_tpe(i)
                    if self.method == "2":
                        self.do_mutation_mac_replace(i)
            self.do_selection_roulette()
            self.generation_runtime[g, 1] = time.perf_counter()
            self.update_generation(g)
            if g >= self.stop_max_stay and np.std(self.generation_objective[g - self.stop_max_stay + 1:g + 1, 0]) == 0:
                k = np.arange(g + 1, self.stop_max_generation + 1)
                self.generation_objective = np.delete(self.generation_objective, k, axis=0)
                self.generation_runtime = np.delete(self.generation_runtime, k, axis=0)
                break
        self.global_best_info.std_code()
        self.global_best_osc = self.global_best_info.osc
        if self.method in ["1", "3", ]:
            self.global_best_mac = self.global_best_info.mac_info
        for i in range(self.pop_size):
            self.pop_info[i].std_code()
            self.pop_osc[i] = self.pop_info[i].osc
            if self.method in ["1", "3", ]:
                self.pop_mac[i] = self.pop_info[i].mac_info


class GaFsp(Ga, Fsp):
    """
    流水车间调度的遗传算法
    """

    def __init__(self, para, data, ):
        pop_size = para[GaName.pop_size]
        rate_crossover = para[GaName.rate_crossover]
        rate_mutation = para[GaName.rate_mutation]
        operator_crossover = para[GaName.operator_crossover]
        operator_mutation = para[GaName.operator_mutation]
        operator_selection = para[GaName.operator_selection]
        stop_max_generation = para[GaName.stop_max_generation]
        stop_max_stay = para[GaName.stop_max_stay]
        function_objective = para[GaName.function_objective]
        Ga.__init__(self, pop_size, rate_crossover, rate_mutation, operator_crossover, operator_mutation,
                    operator_selection, stop_max_generation, stop_max_stay, function_objective, )
        Fsp.__init__(self, data[DataName.n], data[DataName.m],
                     data[DataName.ops], data[DataName.prt], )
        # 定义
        self.pop_job = np.zeros([self.pop_size, self.n], dtype=int)

    def update_info(self, i, obj_new, info_new, job_new, ):
        if Utils.update_info(self.pop_objective[i], obj_new):
            self.pop_info[i] = info_new
            self.pop_job[i] = job_new
            self.pop_objective[i] = obj_new
            self.pop_fitness[i] = Utils.calculate_fitness(obj_new)

    def do_init(self, ):
        self.generation_runtime[0, 0] = time.perf_counter()
        for i in range(self.pop_size):
            self.pop_job[i] = self.code_job_fsp()
            info = self.decode_fsp(self.pop_job[i])
            self.pop_info.append(info)
            self.pop_objective[i] = self.function_objective(info)
            self.pop_fitness[i] = Utils.calculate_fitness(self.pop_objective[i])
        self.generation_runtime[0, 1] = time.perf_counter()
        self.update_generation(0)

    def do_selection_roulette(self, ):
        a = self.selection_roulette()
        pop_osc = deepcopy(self.pop_job)
        pop_objective = deepcopy(self.pop_objective)
        pop_fitness = deepcopy(self.pop_fitness)
        pop_info = deepcopy(self.pop_info)
        for i in range(self.pop_size):
            j = np.argwhere(a[:, 0] > np.random.random())[0, 0]
            self.pop_job[i] = pop_osc[j]
            self.pop_objective[i] = pop_objective[j]
            self.pop_fitness[i] = pop_fitness[j]
            self.pop_info[i] = pop_info[j]
        index = int(np.argmax(self.pop_fitness[:, 0]))
        self.pop_info[index] = self.global_best_info
        self.pop_job[index] = self.global_best_osc[:self.n]
        self.pop_objective[index] = self.global_best_obj
        self.pop_fitness[index] = self.global_best_fitness

    def do_crossover_pmx(self, i, j, ):
        job1, job2 = self.pop_info[i].crossover_pmx_job(self.pop_info[j])
        info1 = self.decode_fsp(job1)
        obj1 = self.function_objective(info1)
        self.update_info(i, obj1, info1, job1)
        info2 = self.decode_fsp(job2)
        obj2 = self.function_objective(info2)
        self.update_info(j, obj2, info2, job2)

    def do_mutation_tpe(self, i, ):
        job1 = self.pop_info[i].mutation_tpe_job()
        info1 = self.decode_fsp(job1)
        obj1 = self.function_objective(info1)
        self.update_info(i, obj1, info1, job1)

    def start_generation(self, ):
        self.do_init()
        for g in range(1, self.stop_max_generation + 1):
            self.generation_runtime[g, 0] = time.perf_counter()
            for i in range(self.pop_size):
                if np.random.random() < self.rate_crossover:
                    j = np.random.choice(np.delete(np.arange(self.pop_size), i), 1, replace=False)[0]
                    self.do_crossover_pmx(i, j)
                if np.random.random() < self.rate_mutation:
                    self.do_mutation_tpe(i)
            self.do_selection_roulette()
            self.generation_runtime[g, 1] = time.perf_counter()
            self.update_generation(g)
            if g >= self.stop_max_stay and np.std(self.generation_objective[g - self.stop_max_stay + 1:g + 1, 0]) == 0:
                k = np.arange(g + 1, self.stop_max_generation + 1)
                self.generation_objective = np.delete(self.generation_objective, k, axis=0)
                self.generation_runtime = np.delete(self.generation_runtime, k, axis=0)
                break


class GaHFsp(Ga, HFsp):
    """
    混合流水车间调度的遗传算法
    """

    def __init__(self, para, data, ):
        pop_size = para[GaName.pop_size]
        rate_crossover = para[GaName.rate_crossover]
        rate_mutation = para[GaName.rate_mutation]
        operator_crossover = para[GaName.operator_crossover]
        operator_mutation = para[GaName.operator_mutation]
        operator_selection = para[GaName.operator_selection]
        stop_max_generation = para[GaName.stop_max_generation]
        stop_max_stay = para[GaName.stop_max_stay]
        function_objective = para[GaName.function_objective]
        Ga.__init__(self, pop_size, rate_crossover, rate_mutation, operator_crossover, operator_mutation,
                    operator_selection, stop_max_generation, stop_max_stay, function_objective, )
        HFsp.__init__(self, data[DataName.n], data[DataName.m], data[DataName.p],
                      data[DataName.ops_list], data[DataName.prt_list], )
        # 定义
        self.pop_job = np.zeros([self.pop_size, self.n], dtype=int)

    def update_info(self, i, obj_new, info_new, job_new, ):
        if Utils.update_info(self.pop_objective[i], obj_new):
            self.pop_info[i] = info_new
            self.pop_job[i] = job_new
            self.pop_objective[i] = obj_new
            self.pop_fitness[i] = Utils.calculate_fitness(obj_new)

    def do_init(self, ):
        self.generation_runtime[0, 0] = time.perf_counter()
        for i in range(self.pop_size):
            self.pop_job[i] = self.code_job_fsp()
            info = self.decode_hfsp(self.pop_job[i])
            self.pop_info.append(info)
            self.pop_objective[i] = self.function_objective(info)
            self.pop_fitness[i] = Utils.calculate_fitness(self.pop_objective[i])
        self.generation_runtime[0, 1] = time.perf_counter()
        self.update_generation(0)

    def do_selection_roulette(self, ):
        a = self.selection_roulette()
        pop_osc = deepcopy(self.pop_job)
        pop_objective = deepcopy(self.pop_objective)
        pop_fitness = deepcopy(self.pop_fitness)
        pop_info = deepcopy(self.pop_info)
        for i in range(self.pop_size):
            j = np.argwhere(a[:, 0] > np.random.random())[0, 0]
            self.pop_job[i] = pop_osc[j]
            self.pop_objective[i] = pop_objective[j]
            self.pop_fitness[i] = pop_fitness[j]
            self.pop_info[i] = pop_info[j]
        index = int(np.argmax(self.pop_fitness[:, 0]))
        self.pop_info[index] = self.global_best_info
        self.pop_job[index] = self.global_best_osc[:self.n]
        self.pop_objective[index] = self.global_best_obj
        self.pop_fitness[index] = self.global_best_fitness

    def do_crossover_pmx(self, i, j, ):
        job1, job2 = self.pop_info[i].crossover_pmx_job(self.pop_info[j])
        info1 = self.decode_hfsp(job1)
        obj1 = self.function_objective(info1)
        self.update_info(i, obj1, info1, job1)
        info2 = self.decode_hfsp(job2)
        obj2 = self.function_objective(info2)
        self.update_info(j, obj2, info2, job2)

    def do_mutation_tpe(self, i, ):
        job1 = self.pop_info[i].mutation_tpe_job()
        info1 = self.decode_hfsp(job1)
        obj1 = self.function_objective(info1)
        self.update_info(i, obj1, info1, job1)

    def start_generation(self, ):
        self.do_init()
        for g in range(1, self.stop_max_generation + 1):
            self.generation_runtime[g, 0] = time.perf_counter()
            for i in range(self.pop_size):
                if np.random.random() < self.rate_crossover:
                    j = np.random.choice(np.delete(np.arange(self.pop_size), i), 1, replace=False)[0]
                    self.do_crossover_pmx(i, j)
                if np.random.random() < self.rate_mutation:
                    self.do_mutation_tpe(i)
            self.do_selection_roulette()
            self.generation_runtime[g, 1] = time.perf_counter()
            self.update_generation(g)
            if g >= self.stop_max_stay and np.std(self.generation_objective[g - self.stop_max_stay + 1:g + 1, 0]) == 0:
                k = np.arange(g + 1, self.stop_max_generation + 1)
                self.generation_objective = np.delete(self.generation_objective, k, axis=0)
                self.generation_runtime = np.delete(self.generation_runtime, k, axis=0)
                break
