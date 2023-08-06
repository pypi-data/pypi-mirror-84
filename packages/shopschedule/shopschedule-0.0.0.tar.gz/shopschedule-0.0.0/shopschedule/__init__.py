import copy
import datetime
import os

import chardet
import matplotlib.pyplot as plt
import numpy as np
import plotly as py
import plotly.figure_factory as ff
from colorama import init, Fore
from matplotlib import colors as mcolors
from .name import ScheduleName

deepcopy = copy.deepcopy
pyplt = py.offline.plot
dt = datetime.datetime
tmdelta = datetime.timedelta
COLORS = list(mcolors.CSS4_COLORS)
LEN_COLORS = len(COLORS)
init(autoreset=True)
np.set_printoptions(precision=2)


class Utils:
    @staticmethod
    def make_dir(dir_name):
        try:
            os.mkdir("./%s" % dir_name)
        except FileExistsError:
            pass

    @staticmethod
    def print(msg, fore=Fore.LIGHTCYAN_EX, ):
        print(fore + msg)

    @staticmethod
    def calculate_fitness(obj):
        return 1 / (1 + obj)

    @staticmethod
    def update_info(old_obj, new_obj):
        if new_obj < old_obj:
            return True
        return False

    @staticmethod
    def load_text(file_name):
        try:
            with open(file_name, "rb") as f:
                f_read = f.read()
                f_cha_info = chardet.detect(f_read)
                final_data = f_read.decode(f_cha_info['encoding'])
                return final_data, True
        except FileNotFoundError:
            return str(None), False

    @staticmethod
    def figure_png(file_name="Figure", dpi=200, ):
        ax = plt.gca()
        [ax.spines[name].set_color('none') for name in ["top", "right", "bottom", "left"]]
        Utils.make_dir("Figure")
        plt.savefig("./Figure/%s" % file_name, dpi=dpi, )
        plt.clf()

    @staticmethod
    def string2data_jsp_fsp(string, add_one=False, minus_one=False, ):
        try:
            to_float = [float(i) for i in string.split()]
            n, m = int(to_float[0]), int(to_float[1])
            ops_prt = np.array(to_float[2:]).reshape(n, -1)
            if add_one is True:
                ops = ops_prt[:, ::2] + 1
            elif minus_one is True:
                ops = ops_prt[:, ::2] - 1
            else:
                ops = ops_prt[:, ::2]
            ops = np.array(ops, dtype=int)
            prt = ops_prt[:, 1::2]
            return n, m, None, ops, prt
        except ValueError:
            return None, None, None, None, None

    @staticmethod
    def string2data_fjsp_hfsp(string, add_one=False, minus_one=True, ):
        try:
            to_float = [float(i) for i in string.split()]
            job, p_list, ops_list, prt_list = 0, [], [], []
            n, m = int(to_float[0]), int(to_float[1])
            index_no, index_nm, index_m, index_t = 2, 3, 4, 5
            while job < n:
                p_list.append(int(to_float[index_no]))
                ops_list.append([])
                prt_list.append([])
                for i in range(p_list[job]):
                    ops_list[job].append([])
                    prt_list[job].append([])
                    int_index_nm = int(to_float[index_nm])
                    for j in range(int_index_nm):
                        int_index_m = int(to_float[index_m])
                        if minus_one is True:
                            ops_list[job][i].append(int_index_m - 1)
                        elif add_one is True:
                            ops_list[job][i].append(int_index_m + 1)
                        else:
                            ops_list[job][i].append(int_index_m)
                        prt_list[job][i].append(to_float[index_t])
                        index_m += 2
                        index_t += 2
                    index_nm = index_nm + 2 * int_index_nm + 1
                    index_m = index_nm + 1
                    index_t = index_nm + 2
                job += 1
                index_nm = index_nm + 1
                index_m = index_m + 1
                index_t = index_t + 1
                index_no = index_t - 3
            return n, m, p_list, ops_list, prt_list
        except ValueError:
            return None, None, None, None, None

    @staticmethod
    def crt_data_jsp(n, m, low, high, ):
        ops = np.tile(np.arange(m), (n, 1))
        for i in range(n):
            ops[i] = ops[i, np.random.permutation(m)]
        prt = np.random.uniform(low, high + 1, [n, m])
        return ops, prt

    @staticmethod
    def crt_data_fjsp(n, m, min_operation, max_operation, operation_max_machine, low, high, ):
        p_list = np.random.randint(min_operation, max_operation + 1, n)
        p_list = [i for i in p_list]
        ops_list, prt_list = [], []
        for i in range(n):
            ops_list.append([[]])
            prt_list.append([[]])
        for i, j in enumerate(p_list):
            ops_list[i] = ops_list[i] * j
            prt_list[i] = prt_list[i] * j
        for i in range(n):
            machines = np.arange(m)
            for j in range(p_list[i]):
                n_machines = np.random.randint(1, operation_max_machine + 1)
                if len(machines) >= n_machines:
                    ops_list[i][j] = np.random.choice(machines, n_machines, replace=False).tolist()
                else:
                    machines = np.arange(m)
                    ops_list[i][j] = np.random.choice(machines, n_machines, replace=False).tolist()
                for k in ops_list[i][j]:
                    d = np.argwhere(machines == k)[:, 0]
                    machines = np.delete(machines.copy(), d)
                value1 = np.random.uniform(low, high + 1, 1)
                if value1 < 50:
                    value2 = max([1, int(0.9 * value1)])
                    value3 = max([1, int(1.1 * value1)])
                else:
                    value2 = int(0.95 * value1)
                    value3 = int(1.05 * value1)
                prt_list[i][j] = np.random.choice([value1[0], value2, value3], n_machines)
        return p_list, ops_list, prt_list

    @staticmethod
    def crt_data_fsp(n, m, low, high, ):
        a = np.tile(range(m), (n, 1))
        b = np.random.uniform(low, high + 1, [n, m])
        return a, b

    @staticmethod
    def crt_data_hfsp(n, m, p, m_min, m_max, low, high, ):
        ops_list = []
        prt_list = []
        m_list = []
        for i in range(p):
            m_list.append(np.random.randint(m_min, m_max + 1))
        for i in range(n):
            ops_list.append([])
            prt_list.append([])
            m = 0
            for j in range(p):
                m_range = list(range(m, m + m_list[j]))
                ops_list[i].append(m_range)
                value1 = np.random.uniform(low, high + 1, 1)
                if value1 < 50:
                    value2 = max([1, int(0.9 * value1)])
                    value3 = max([1, int(1.1 * value1)])
                else:
                    value2 = int(0.95 * value1)
                    value3 = int(1.05 * value1)
                prt_list[i].append(np.random.choice([value1[0], value2, value3], m_list[j]).tolist())
                m += m_list[j]
        return ops_list, prt_list


class Info:
    """
    调度信息
    """

    def __init__(self, name, n, m, length, osc, opr, mac, proc, start, finish, job_index, machine_index,
                 mit_start=None, mit_time=None, mac_to1=None, ops_list=None, p=None, ):
        """
        初始化
        :param name: 车间类型
        :param n: 工件数量
        :param m: 机器数量
        :param length: 工序数量
        :param osc: 工件
        :param opr:工序
        :param mac: 机器
        :param proc: 加工时间
        :param start: 加工开始时刻
        :param finish: 加工完成时刻
        :param job_index: 工件索引
        :param machine_index: 机器索引
        :param mit_start: 机器空闲时段的开始时刻
        :param mit_time: 机器空闲时段的空闲时间
        :param mac_to1: 柔性作业作业的第二类机器编码转化为第一类机器编码
        :param ops_list: 加工机器集合
        :param p: 工序数量
        """
        self.name = name
        self.n = n
        self.m = m
        self.p = p
        self.length = length
        self.osc = deepcopy(osc)
        self.opr = deepcopy(opr)
        self.mac = deepcopy(mac)
        self.ops_list = deepcopy(ops_list)
        if mac_to1 is None:
            self.mac_info = deepcopy(mac)
        else:
            self.mac_info = deepcopy(mac_to1)
        self.proc = deepcopy(proc)
        self.start = deepcopy(start)
        self.finish = deepcopy(finish)
        self.mit_start = deepcopy(mit_start)
        self.mit_time = deepcopy(mit_time)
        self.job_index = deepcopy(job_index)
        self.machine_index = deepcopy(machine_index)
        # 定义
        self.makespan = max(self.finish)  # 生产周期

    # 【标准化编码】
    def std_code(self, ):
        index = np.argsort(self.start)
        self.osc = self.osc[index]
        self.opr = self.opr[index]
        self.mac_info = self.mac_info[index]
        self.proc = self.proc[index]
        self.start = self.start[index]
        self.finish = self.finish[index]
        self.job_index = []
        self.machine_index = []
        for i in range(self.n):
            self.job_index.append([])
        for i in range(self.m):
            self.machine_index.append([])
        for i in range(self.length):
            self.job_index[self.osc[i]].append(i)
            self.machine_index[self.mac_info[i]].append(i)

    # 【遗传算法】交叉操作
    def crossover_pox_osc(self, info2, ):
        osc1 = deepcopy(self.osc)
        osc2 = deepcopy(info2.osc)
        a = np.random.choice(self.n, 1, replace=False)
        b, c = np.argwhere(osc1 != a)[:, 0], np.argwhere(osc2 != a)[:, 0]
        osc1[b], osc2[c] = osc2[c], osc1[b]
        return osc1, osc2

    def crossover_ipox_osc(self, info2, ):
        osc1 = deepcopy(self.osc)
        osc2 = deepcopy(info2.osc)
        a = np.random.choice(self.n, 2, replace=False)
        b, c = [[], []], [osc1, osc2]
        for i in range(2):
            for j in range(2):
                index = np.argwhere(c[j] == a[i])[:, 0]
                b[j].extend(index.tolist())
        d = np.delete(range(self.length), b[0])
        e = np.delete(range(self.length), b[1])
        osc1[d], osc2[e] = osc2[e], osc1[d]
        return osc1, osc2

    def crossover_pmx_job(self, info2, ):
        job1 = deepcopy(self.osc[:self.n])
        job2 = deepcopy(info2.osc[:self.n])
        a, b = np.random.choice(self.n, 2, replace=False)
        min_a_b, max_a_b = min([a, b]), max([a, b])
        r_a_b = range(min_a_b, max_a_b)
        r_left = np.delete(range(self.n), r_a_b)
        left_1, left_2 = job2[r_left], job1[r_left]
        middle_1, middle_2 = job2[r_a_b], job1[r_a_b]
        job1[r_a_b], job2[r_a_b] = middle_2, middle_1
        mapping = [[], []]
        for i, j in zip(middle_1, middle_2):
            if j in middle_1 and i not in middle_2:
                index = np.argwhere(middle_1 == j)[0, 0]
                value = middle_2[index]
                while True:
                    if value in middle_1:
                        index = np.argwhere(middle_1 == value)[0, 0]
                        value = middle_2[index]
                    else:
                        break
                mapping[0].append(i)
                mapping[1].append(value)
            elif i in middle_2:
                pass
            else:
                mapping[0].append(i)
                mapping[1].append(j)
        for i, j in zip(mapping[0], mapping[1]):
            if i in left_1:
                left_1[np.argwhere(left_1 == i)[0, 0]] = j
            elif i in left_2:
                left_2[np.argwhere(left_2 == i)[0, 0]] = j
            if j in left_1:
                left_1[np.argwhere(left_1 == j)[0, 0]] = i
            elif j in left_2:
                left_2[np.argwhere(left_2 == j)[0, 0]] = i
        job1[r_left], job2[r_left] = left_1, left_2
        return job1, job2

    def crossover_random_mac1(self, info2, ):  # 基于第一类机器编码的交叉
        mac1 = deepcopy(self.mac)
        mac2 = deepcopy(info2.mac)
        # Todo: 实现
        return mac1, mac2

    def crossover_random_mac2(self, info2, ):  # 基于第二类机器编码的交叉
        mac1 = deepcopy(self.mac)
        mac2 = deepcopy(info2.mac)
        # Todo: 改进
        for i, (p, q) in enumerate(zip(mac1, mac2)):
            for j, (u, v) in enumerate(zip(p, q)):
                if np.random.random() < 0.5:
                    mac1[i][j], mac2[i][j] = v, u
        return mac1, mac2

    # 【遗传算法】变异操作
    def mutation_tpe_osc(self, ):
        osc = deepcopy(self.osc)
        a = np.random.choice(self.length, 2, replace=False)
        osc[a] = osc[a[::-1]]
        return osc

    def mutation_tpe_job(self, ):
        job = deepcopy(self.osc[:self.n])
        a = np.random.choice(self.n, 2, replace=False)
        job[a] = job[a[::-1]]
        return job

    def mutation_replace_mac1(self, ):  # 基于第一类机器编码的替换
        mac = deepcopy(self.mac)
        # Todo: 实现
        return mac

    def mutation_replace_mac2(self, ):  # 基于第二类机器编码的替换
        mac = deepcopy(self.mac)
        # Todo: 改进
        a = np.random.choice(self.n, np.random.randint(1, self.n), replace=False)
        for job in a:
            for i, j in enumerate(mac[job]):
                if np.random.random() < 0.5:
                    mac[job][i] = np.random.choice(self.ops_list[job][i], 1, replace=False)[0]
        return mac

    # 关键路径
    def get_one_key_route(self, key_route, mac_seq, num_index_makespan, index_makespan, ):
        if num_index_makespan > 1:
            i = 1
            while True:
                b = np.random.choice(index_makespan, 1, replace=False)[0]
                if b not in key_route or i > num_index_makespan:
                    break
                i += 1
        else:
            b = index_makespan[0]
        if b not in key_route:
            key_route.append(b)
        while True:
            index_op = self.job_index[self.osc[b]][self.opr[b] - 1]
            index_ma = self.machine_index[self.mac_info[b]][mac_seq[b] - 1]
            c = None
            if self.finish[index_op] == self.finish[index_ma] == self.start[b]:
                if index_op not in key_route and index_ma in key_route:
                    c = index_op
                elif index_op in key_route and index_ma not in key_route:
                    c = index_ma
                else:
                    if np.random.random() < 0.5:
                        c = index_op
                    else:
                        c = index_ma
            elif self.finish[index_op] == self.start[b]:
                c = index_op
            elif self.finish[index_ma] == self.start[b]:
                c = index_ma
            if c is not None:
                b = c
                if b not in key_route:
                    key_route.append(b)
            else:
                break
        return key_route

    def get_all_key_route(self, n=5, ):
        self.std_code()
        mac_seq = np.zeros(self.length, dtype=int)
        for i in range(self.m):
            index = np.argwhere(self.mac_info == i)[:, 0]
            mac_seq[index] = range(index.shape[0])
        index_makespan = np.argwhere(self.finish == self.makespan)[:, 0]
        num_index_makespan = len(index_makespan)
        key_route = []
        key_block = np.zeros(self.length, dtype=int)
        for _ in range(n):
            key_route = self.get_one_key_route(key_route, mac_seq, num_index_makespan, index_makespan)
        block = 1
        mac = self.mac_info[key_route]
        start = self.start[key_route]
        finish = self.finish[key_route]
        key_route = np.array(key_route)
        machines = set(mac)
        for i in machines:
            index_i = np.argwhere(mac == i)[:, 0]
            len_index_i = len(index_i)
            key_route_i = key_route[index_i]
            if len_index_i > 0:
                start_i = start[index_i]
                finish_i = finish[index_i]
                sort_index = np.argsort(start_i)
                start_i = start_i[sort_index]
                finish_i = finish_i[sort_index]
                key_route_i = key_route_i[sort_index]
                for j in range(len_index_i):
                    if j > 0 and start_i[j] != finish_i[j - 1]:
                        block += 1
                    key_block[key_route_i[j]] = block
            else:
                block += 1
                key_block[key_route_i[0]] = block
            block += 1
        return set(key_route), key_block

    # 【甘特图】png格式
    def ganttChart_png(self, file_name="GanttChart", dpi=200, ):
        np.random.shuffle(COLORS)
        plt.figure(figsize=[9, 5])
        plt.margins()
        plt.tight_layout()
        ymin = -0.5
        ymax = self.m + ymin
        plt.vlines(self.makespan, ymin, ymax, colors="red", linestyles="--")
        plt.text(self.makespan, ymin, round(self.makespan, 2))
        key_route, key_block = self.get_all_key_route()
        for i in range(self.length):
            color_bar = COLORS[self.osc[i] % LEN_COLORS]
            if i in key_route:
                edgecolor, text_color = COLORS[(key_block[i] - 1) % LEN_COLORS], "red"
            else:
                edgecolor, text_color = color_bar, "black"
            width = self.finish[i] - self.start[i]  # self.duration[i]
            plt.barh(y=self.mac_info[i], width=width, left=self.start[i],
                     color=color_bar, edgecolor=edgecolor)
            if self.name in [ScheduleName.jsp, ScheduleName.fjsp, ]:
                text = r"$O_{%s,%s}$" % (self.osc[i] + 1, self.opr[i] + 1)
            else:
                text = r"${%s}$" % (self.osc[i] + 1)
            plt.text(x=self.start[i] + 0.5 * width, y=self.mac_info[i],
                     s=text, c=text_color,
                     ha="center", va="center", )
        if self.name in [ScheduleName.jsp, ScheduleName.fjsp, ScheduleName.fsp, ]:
            plt.yticks(range(self.m), range(1, self.m + 1))
        else:
            yticks = []
            for i in range(self.p):
                for j in range(len(self.ops_list[0][i])):
                    msg = "${%s}^{%s}$" % (i + 1, j + 1)
                    yticks.append(msg)
            plt.yticks(range(self.m), yticks)
        plt.xticks([], [])
        Utils.figure_png(file_name=file_name, dpi=dpi)

    # 【甘特图】html格式
    @property
    def rgb(self, ):
        return np.random.randint(0, 256)

    def ganttChart_html(self, date=None, file_name="GanttChart", auto_open=False, ):
        if date is None:
            today = dt.today()
            date = dt(today.year, today.month, today.day)
        df = []
        colors = {}
        for machine in np.arange(self.m - 1, -1, -1):
            for i in self.machine_index[machine]:
                df.append(dict(Task="M%s" % (machine + 1), Start=date + tmdelta(0, int(self.start[i])),
                               Finish=date + tmdelta(0, int(self.finish[i])),
                               Resource="%s" % (self.osc[i] + 1), complete=self.osc[i] + 1))
        for i in range(self.n):
            key = "%s" % (i + 1)
            colors[key] = "rgb(%s, %s, %s)" % (self.rgb, self.rgb, self.rgb)
        fig = ff.create_gantt(df, colors=colors, index_col='Resource', group_tasks=True, show_colorbar=True)
        Utils.make_dir("GanttChart")
        pyplt(fig, filename=r"./GanttChart/%s.html" % file_name, auto_open=auto_open)


class Objective:
    """
    目标函数
    :return:
    """

    @staticmethod
    def makespan(info):
        return info.makespan


class Jsp:
    """
    Job shop scheduling problem（作业车间调度问题）
    """
    name = ScheduleName.jsp

    def __init__(self, n, m, ops, prt, ):
        """
        初始化
        :param n: 工件数量
        :param m: 机器数量
        :param ops: 工艺路线
        :param prt: 加工时间
        """
        self.n = n
        self.m = m
        self.ops = ops
        self.prt = prt
        # 定义
        self.length = self.n * self.m  # 编码长度

    def code_osc_jsp(self, ):
        """
        基于工序的编码
        :return:
        """
        return np.tile(np.arange(self.n), self.m)[np.random.permutation(self.length)]

    def decode_jsp(self, osc, ):
        """
        解码
        :param osc: 编码
        :return:
        """
        opr = np.zeros(self.length, dtype=int)  # 工序编号
        job_index = []  # 工件索引
        machine_index = []  # 机器索引
        mit_start = []  # 机器空闲时段的开始时刻
        mit_time = []  # 机器空闲时段的空闲时间
        for i in range(self.m):
            machine_index.append([])
            mit_start.append([])
            mit_time.append([])
        for i in range(self.n):
            index = np.argwhere(osc == i)[:, 0]
            opr[index] = range(index.shape[0])
            job_index.append([])
        mac = self.ops[osc, opr]  # 机器编号
        proc = self.prt[osc, opr]  # 加工时间
        start = np.zeros(self.length)  # 加工开始时刻
        finish = np.zeros(self.length)  # 加工完成时刻
        for i in range(self.length):
            job = osc[i]
            operation = opr[i]
            machine = mac[i]
            duration = proc[i]
            try:  # 工件前序工序加工完成时刻
                f1 = finish[job_index[job][operation - 1]]
            except IndexError:
                f1 = 0
            try:  # 机器上的最大完工时可
                f2 = max(finish[machine_index[machine]])
            except ValueError:
                f2 = 0
            start[i] = max([f1, f2])
            insert_index = None
            # 主动解码
            for r, (s, t) in enumerate(zip(mit_start[machine], mit_time[machine])):
                e = s + t
                if s >= f1 and t >= duration or (
                        s < f1 and e >= f1 + duration):
                    start[i] = max([s, f1])
                    insert_index = r
                    break
            finish[i] = start[i] + duration
            job_index[job].append(i)
            machine_index[machine].append(i)
            if insert_index is not None:
                copy_mit_time = deepcopy(mit_time[machine][insert_index])
                mit_time[machine][insert_index] = start[i] - mit_start[machine][insert_index]
                left_idle = copy_mit_time - (finish[i] - mit_start[machine][insert_index])
                if mit_time[machine][insert_index] == 0:
                    mit_start[machine].pop(insert_index)
                    mit_time[machine].pop(insert_index)
                if left_idle > 0:
                    mit_start[machine].insert(insert_index, finish[i])
                    mit_time[machine].insert(insert_index, left_idle)
            elif start[i] - f2 > 0:
                mit_start[machine].append(f2)
                mit_time[machine].append(start[i] - f2)
        return Info(self.name, self.n, self.m, self.length,
                    osc, opr, mac, proc, start, finish,
                    job_index, machine_index,
                    mit_start=mit_start,
                    mit_time=mit_time, )


class FJsp:
    """
    Flexible job shop scheduling problem（柔性作业车间调度问题）
    """
    name = ScheduleName.fjsp

    def __init__(self, n, m, p_list, ops_list, prt_list, ):
        """
        初始化
        :param n: 工件数量
        :param m: 机器数量
        :param p_list: 工序数量
        :param ops_list: 工艺路线
        :param prt_list: 加工时间
        """
        self.n = n
        self.m = m
        self.p_list = p_list
        self.ops_list = ops_list
        self.prt_list = prt_list
        # 定义
        self.length = sum(self.p_list)  # 编码长度

    def code_osc_fjsp(self, ):
        """
        基于工序的编码
        :return:
        """
        a = []
        for i, j in enumerate(self.p_list):
            a.extend([i] * j)
        np.random.shuffle(a)
        return np.array(a)

    def code_mac1_fjsp(self, osc, ):
        """
        第一类机器编码，一一对应
        :return:
        """
        a = np.zeros(self.length, dtype=int)  # 机器编码
        b = np.zeros(self.length, dtype=int)
        for i in range(self.n):
            index = np.argwhere(osc == i)[:, 0]
            b[index] = range(index.shape[0])
        for i, j in enumerate(osc):
            a[i] = np.random.choice(self.ops_list[j][b[i]], 1, replace=False)[0]
        return a

    def code_mac2_fjsp(self, ):
        """
        第二类机器编码，按工件划分
        :return:
        """
        a = []
        for i in range(self.n):
            a.append([])
            for j, k in enumerate(self.ops_list[i]):
                a[i].append(np.random.choice(k, 1, replace=False)[0])
        return a

    def decode_fjsp(self, osc, mac=None, method="1", ):
        """
        解码
        :param osc:
        :param mac:
        :param method:
                    1:基于第一类机器编码
                    2:基于第二类机器编码
                    3:基于最早完工时刻指派机器
        :return:
        """
        opr = np.zeros(self.length, dtype=int)  # 工序编号
        if method == "2":
            mac_to1 = np.zeros(self.length, dtype=int)  # 机器编号
        else:
            mac_to1 = None
        job_index = []  # 工件索引
        machine_index = []  # 机器索引
        mit_start = []  # 机器空闲时段的开始时刻
        mit_time = []  # 机器空闲时段的空闲时间
        for i in range(self.m):
            machine_index.append([])
            mit_start.append([])
            mit_time.append([])
        for i in range(self.n):
            index = np.argwhere(osc == i)[:, 0]
            opr[index] = range(index.shape[0])
            if method == "2":
                mac_to1[index] = mac[i]
            job_index.append([])
        proc = np.zeros(self.length)  # 加工时间
        start = np.zeros(self.length)  # 加工开始时刻
        finish = np.zeros(self.length)  # 加工完成时刻
        if method in ["3", ]:
            mac = np.zeros(self.length, dtype=int)  # 机器编号
            cur_job = np.zeros(self.n)  # 工件当前最大完工时刻
            cur_mac = np.zeros(self.m)  # 机器当前最大完工时刻
            for i in range(self.length):
                job = osc[i]
                operation = opr[i]
                mac_list = self.ops_list[job][operation]
                duration_list = []
                start_list = []
                finish_list = []
                insert_index = []
                f1 = cur_job[job]
                for p, q in enumerate(mac_list):
                    duration_time = self.prt_list[job][operation][p]
                    start_time = max([f1, cur_mac[q]])
                    try_insert = False
                    for r, (s, t) in enumerate(zip(mit_start[q], mit_time[q])):
                        e = s + t
                        if s >= f1 and t >= duration_time or (
                                s < f1 and e >= f1 + duration_time):
                            start_time = max([s, f1])
                            insert_index.append(r)
                            try_insert = True
                            break
                    finish_time = start_time + duration_time
                    if try_insert is False:
                        insert_index.append(-1)
                    duration_list.append(duration_time)
                    start_list.append(start_time)
                    finish_list.append(finish_time)
                min_finish = min(finish_list)
                index = np.argwhere(np.array(finish_list) == min_finish)[:, 0]
                choice = np.random.choice(index, 1)[0]
                machine = mac_list[choice]
                cur_job[job] = min_finish
                try:
                    cur_mac[machine] = max([min_finish, np.max(finish[machine_index[machine]])])
                except ValueError:
                    cur_mac[machine] = min_finish
                mac[i] = machine
                proc[i] = duration_list[choice]
                start[i] = start_list[choice]
                finish[i] = finish_list[choice]
                insert_position = insert_index[choice]
                job_index[job].append(i)
                machine_index[machine].append(i)
                if insert_position != -1:
                    copy_mit_time = copy.deepcopy(mit_time[machine][insert_position])
                    mit_time[machine][insert_position] = start[i] - mit_start[machine][insert_position]
                    left_idle = copy_mit_time - (finish[i] - mit_start[machine][insert_position])
                    if mit_time[machine][insert_position] == 0:
                        mit_start[machine].pop(insert_position)
                        mit_time[machine].pop(insert_position)
                    if left_idle > 0:
                        mit_start[machine].insert(insert_position, finish[i])
                        mit_time[machine].insert(insert_position, left_idle)
                else:
                    mac_finish = finish[machine_index[machine]]
                    sort_index = np.argsort(mac_finish)
                    try:
                        pre_finish = mac_finish[sort_index[-2]]
                        if start[i] - pre_finish > 0:
                            mit_start[machine].append(pre_finish)
                            mit_time[machine].append(start[i] - pre_finish)
                    except IndexError:
                        try:
                            first_start = np.min(start[machine_index[machine]])
                        except ValueError:
                            first_start = None
                        if first_start is not None and first_start > 0:
                            mit_start[machine].append(0)
                            mit_time[machine].append(first_start)
        else:
            for i in range(self.length):
                job = osc[i]
                operation = opr[i]
                if method == "2":
                    machine = mac_to1[i]  # 基于第二类机器编码
                else:
                    machine = mac[i]  # 基于第一类机器编码
                index = np.argwhere(self.ops_list[job][operation] == machine)[0, 0]
                duration = self.prt_list[job][operation][index]
                proc[i] = duration
                try:
                    f1 = finish[job_index[job][operation - 1]]
                except IndexError:
                    f1 = 0
                try:
                    f2 = max(finish[machine_index[machine]])
                except ValueError:
                    f2 = 0
                start[i] = max([f1, f2])
                insert_index = None
                for r, (s, t) in enumerate(zip(mit_start[machine], mit_time[machine])):
                    e = s + t
                    if s >= f1 and t >= duration or (
                            s < f1 and e >= f1 + duration):
                        start[i] = max([s, f1])
                        insert_index = r
                        break
                finish[i] = start[i] + duration
                job_index[job].append(i)
                machine_index[machine].append(i)
                if insert_index is not None:
                    copy_mit_time = deepcopy(mit_time[machine][insert_index])
                    mit_time[machine][insert_index] = start[i] - mit_start[machine][insert_index]
                    left_idle = copy_mit_time - (finish[i] - mit_start[machine][insert_index])
                    if mit_time[machine][insert_index] == 0:
                        mit_start[machine].pop(insert_index)
                        mit_time[machine].pop(insert_index)
                    if left_idle > 0:
                        mit_start[machine].insert(insert_index, finish[i])
                        mit_time[machine].insert(insert_index, left_idle)
                elif start[i] - f2 > 0:
                    mit_start[machine].append(f2)
                    mit_time[machine].append(start[i] - f2)
        return Info(self.name, self.n, self.m, self.length,
                    osc, opr, mac, proc, start, finish,
                    job_index, machine_index,
                    mit_start=mit_start,
                    mit_time=mit_time,
                    mac_to1=mac_to1,
                    ops_list=self.ops_list, )


class Fsp:
    """
    Flow shop scheduling problem（流水车间调度问题）
    """
    name = ScheduleName.fsp

    def __init__(self, n, m, ops, prt, ):
        self.n = n
        self.m = m
        self.ops = ops
        self.prt = prt
        self.length = n * m

    def code_job_fsp(self, ):
        return np.random.permutation(self.n)

    def decode_fsp(self, job, ):
        osc = np.tile(job, self.m)
        mac = opr = np.repeat(range(self.m), self.n)
        job_index = []
        for i in range(self.n):
            j = np.argwhere(osc == i)[0, 0]
            k = [j + index * self.n for index in range(self.m)]
            job_index.append(k)
        machine_index = []
        for i in range(self.m):
            j = i * self.n
            machine_index.append(np.arange(j, j + self.n).tolist())
        jpt = self.prt[osc, opr]
        jst = np.zeros([self.n, self.m])
        jft = np.zeros([self.n, self.m])
        for i in range(self.n):
            for j in range(self.m):
                jst[i, j] = max([jft[i, j - 1], jft[i - 1, j]])
                jft[i, j] = jst[i, j] + jpt[i + j * self.n]
        proc = jpt.T.flatten()
        start = jst.T.flatten()
        finish = jft.T.flatten()
        return Info(self.name, self.n, self.m, self.length,
                    osc, opr, mac, proc, start, finish,
                    job_index, machine_index, )


class HFsp:
    """
    Hybrid flow shop scheduling problem（混合流水车间调度问题）
    """
    name = ScheduleName.hfsp

    def __init__(self, n, m, p, ops_list, prt_list):
        self.n = n
        self.m = m
        self.p = p
        self.ops_list = ops_list
        self.prt_list = prt_list
        self.length = n * p

    def code_job_fsp(self, ):
        return np.random.permutation(self.n)

    def decode_hfsp(self, code_job, ):
        osc = np.tile(code_job, self.m)
        opr = np.repeat(range(self.p), self.n)
        mac = np.zeros(self.length, dtype=int)
        job_index = []
        machine_index = []
        for i in range(self.n):
            job_index.append([])
        for i in range(self.m):
            machine_index.append([])
        proc = np.zeros(self.length)
        start = np.zeros(self.length)
        finish = np.zeros(self.length)
        for i in range(self.length):
            job = osc[i]
            operation = opr[i]
            mac_list = self.ops_list[job][operation]
            duration_list = []
            start_list = []
            finish_list = []
            try:
                f1 = finish[job_index[job][operation - 1]]
            except IndexError:
                f1 = 0
            for j, k in enumerate(mac_list):
                duration_time = self.prt_list[job][operation][j]
                try:
                    start_time = max([f1, max(finish[machine_index[k]])])
                except ValueError:
                    start_time = max([0, f1])
                finish_time = start_time + duration_time
                duration_list.append(duration_time)
                start_list.append(start_time)
                finish_list.append(finish_time)
            index = np.argwhere(np.array(finish_list) == min(finish_list))[:, 0]
            choice = np.random.choice(index, 1)[0]
            mac[i] = mac_list[choice]
            proc[i] = duration_list[choice]
            start[i] = start_list[choice]
            finish[i] = finish_list[choice]
            job_index[job].append(i)
            machine_index[mac[i]].append(i)
            if self.length - 1 > i > 0 and (i + 1) % self.n == 0:
                value = osc[i - self.n + 1:i + 1]
                index = np.argsort(finish[i - self.n + 1:i + 1])
                osc[i + 1:i + 1 + self.n] = value[index]
        return Info(self.name, self.n, self.m, self.length,
                    osc, opr, mac, proc, start, finish,
                    job_index, machine_index,
                    ops_list=self.ops_list,
                    p=self.p, )

    def decode_hfsp_osc_mac(self, osc, mac, ):
        opr = np.repeat(range(self.p), self.n)
        mac_seq = np.zeros(self.length, dtype=int)
        for i in range(self.m):
            index = np.argwhere(mac == i)[:, 0]
            mac_seq[index] = range(index.shape[0])
        job_index = []
        machine_index = []
        for i in range(self.n):
            job_index.append([])
        for i in range(self.m):
            machine_index.append([])
        proc = np.zeros(self.length)
        start = np.zeros(self.length)
        finish = np.zeros(self.length)
        for i in range(self.length):
            index = np.argwhere(self.ops_list[osc[i]][opr[i]] == mac[i])[:, 0][0]
            proc[i] = self.prt_list[osc[i]][opr[i]][index]
            try:
                f1 = finish[job_index[osc[i]][opr[i] - 1]]
            except IndexError:
                f1 = 0
            try:
                f2 = finish[machine_index[mac[i]][mac_seq[i] - 1]]
            except IndexError:
                f2 = 0
            start[i] = max([f1, f2])
            finish[i] = start[i] + proc[i]
            job_index[osc[i]].append(i)
            machine_index[mac[i]].append(i)
        return Info(self.name, self.n, self.m, self.length,
                    osc, opr, mac, proc, start, finish,
                    job_index, machine_index,
                    ops_list=self.ops_list,
                    p=self.p, )
