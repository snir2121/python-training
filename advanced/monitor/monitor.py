import csv
import matplotlib.pyplot as plt
import argparse
import psutil
from time import *
import wmi


class Monitor:
    sampled_parameter_options = ["RAM_usage", "CPU_usage", "temperature", "network_usage"]

    def __init__(self, sampled_parameter, running_time=40., sampling_rate=1):
        """
        Initialize method, organizes and checks the input as well.
        :param sampled_parameter: The parameter we want to sample out of :
        ["RAM_usage", "CPU_usage", "temperature", "network_usage"]

        :param running_time: The time (in seconds) that the parameter would be sampled.
        :param sampling_rate: The samples rate.
        """
        self._sampled_parameter = sampled_parameter.replace(" ", "_")
        self._running_time = running_time
        self._sampling_rate = sampling_rate
        self._check_input()

    def _check_input(self):
        """
        Checks if the input is valid.
        """
        # self._sampled_parameter
        if type(self._sampled_parameter) != str:
            raise TypeError("The sampled parameter inserted needs to be a string, not a '%s'"
                            % self._sampled_parameter.__class__.__name__())

        elif self._sampled_parameter not in Monitor.sampled_parameter_options:
            raise ValueError("The sampled parameter can be only one of this parameters: ",
                             Monitor.sampled_parameter_options)

        # self._running_time
        if not (type(self._running_time) == float or type(self._running_time) == int):
            raise TypeError("The running time inserted needs to be a integer or float, not a '%s'"
                            % self._sampled_parameter.__class__.__name__())

        elif self._running_time <= 0:
            raise ValueError("The running time can be only positive")

        # self._sampling_rate
        if not (type(self._sampling_rate) == float or type(self._sampling_rate) == int):
            raise TypeError("The sampling rate inserted needs to be a integer or float, not a '%s'"
                            % self._sampled_parameter.__class__.__name__())

        elif self._sampling_rate <= 0:
            raise ValueError("The running time can be only positive")

        elif not  self._sampling_rate <= 2:
            print("WARNING recommended sampling rate lower then 2 samples per second. ")

    def csv_save_sampling(self, save_graphs=True):
        """
        Saving the results in csv file, save graph - if entered True as a parameter.
        :param save_graphs: If saving graphs is wanted as well.
        :return:
        """
        sampling_func = self._wanted_sampling_func()

        # value_lst = []
        # time_lst = []
        # timer = 0.
        # while timer < self._running_time:  # TODO improve
        #     value = sampling_func()
        #     value_lst.append(value)
        #     time_lst.append(timer)
        #     sleep(1. / self._sampling_rate)
        #     timer += 1. / self._sampling_rate
        #     print(str(timer) + " out of " + str(self._running_time))

        value_lst = []
        time_lst = []
        starting_time = time()
        while time() < starting_time + self._running_time:
            value = sampling_func()
            value_lst.append(value)
            time_lst.append(round(time() - starting_time, 3))
            sleep(1. / self._sampling_rate)
            print(str(round(time() - starting_time, 3)) + " out of " + str(self._running_time))

        result_dict = {self._sampled_parameter: value_lst, "time": time_lst}
        self._csv_save_results(result_dict)

        if save_graphs:
            self._save_graphs(result_dict)

    def _wanted_sampling_func(self):
        """
         Finding the sampling function according to the sampling parameter.
        :return:
        """
        func = lambda: 1
        if self._sampled_parameter == "RAM_usage":
            func = lambda: psutil.virtual_memory()[2]

        elif self._sampled_parameter == "CPU_usage":
            func = lambda: psutil.cpu_percent()

        elif self._sampled_parameter == "temperature":
            func = lambda: psutil.sensors_temperatures()  # TODO check if really not in windows.

        elif self._sampled_parameter == "network_usage":
            func = lambda: psutil.net_io_counters()  # TODO

        return func

    def _name_for_file(self, text="stats", graph=False):
        """
        Returns an appropriate name for a file.
        :param text: An addition if wanted.
        :param graph: If the file is a graph.
        :return:
        """
        if graph:
            return self._sampled_parameter + "_" + text + "_" + strftime("%H;%M;%S-%d;%m;%Y") + ".png"

        return self._sampled_parameter + "_" + text + "_" + strftime("%H;%M;%S-%d;%m;%Y") + ".csv"

    def _csv_save_results(self, result_dict):
        """
        Saving the results in csv.
        :param result_dict: A dictionary with the results.
        """
        with open(self._name_for_file(), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[self._sampled_parameter, "time"])

            writer.writeheader()

            for i in range(len(result_dict[self._sampled_parameter])):

                writer.writerow({self._sampled_parameter: result_dict[self._sampled_parameter][i],
                                'time': result_dict['time'][i]})

    def _save_graphs(self, result_dict):
        """
        Saving the graphs in file.
        :param result_dict: The dictionary with the results.
        :return:
        """

        fig, axs = plt.subplots(2)
        fig.suptitle(self._sampled_parameter + "sampled graphs")

        # Value over time graph
        x = result_dict["time"]
        y = result_dict[self._sampled_parameter]

        axs[0].plot(x, y)
        graph_name = "value over time"
        axs[0].set(title=graph_name, xlabel="time", ylabel=self._sampled_parameter)

        # Hist graph
        y = result_dict[self._sampled_parameter]

        axs[1].hist(y)
        graph_name = "hist"
        axs[1].set(title=graph_name, xlabel=self._sampled_parameter, ylabel="number of times")

        plt.savefig(self._name_for_file("graphs", True))


def main():
    """
    Using commend line interface.
    usage: monitor.py [-h]
                  [--sampled_parameter {RAM_usage,CPU_usage,temperature,network_usage}]
                  [--running_time RUNNING_TIME]
                  [--sampling_rate SAMPLING_RATE]
    :return:
    """
    parser = argparse.ArgumentParser(description='Implementing monitor')
    parser.add_argument("--sampled_parameter", "--sp", type=str,
                        choices=["RAM_usage", "CPU_usage", "temperature", "network_usage"])
    parser.add_argument("--running_time", "--rt", type=float, default=40.)
    parser.add_argument("--sampling_rate", "--sr", type=float, default=1.)
    args = parser.parse_args()

    m = Monitor(args.sampled_parameter, args.running_time, args.sampling_rate)
    m.csv_save_sampling()


if __name__ == '__main__':
    main()
