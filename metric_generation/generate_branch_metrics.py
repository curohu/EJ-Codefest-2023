import csv
from branch_metric import BranchMetric
import sys, getopt
from random import randint


def main(argv):
    opts, args = getopt.getopt(argv, "hi:p:s:f:b:", ["increments=", "period=", "start_timestamp=", "frequency=", "branch_count="])
    increment = 60
    period = 86400
    start_timestamp = 0
    frequency = 2
    branch_count = 5
    for opt, arg in opts:
        if opt == "-h":
            print('generate_branch_metrics.py -i <increments in seconds> -p <total period in seconds> -s <start timestamp> -f <spike frequncy>')
            sys.exit()
        elif opt in ("-i", "--increments"):
            increment = int(arg)
        elif opt in ("-p", "--period"):
            period = int(arg)
        elif opt in ("-s", "--start_timestamp"):
            start_timestamp = int(arg)
        elif opt in ("-f", "--frequency"):
            frequency = int(arg)
        elif opt in ("-b", "--branch_count"):
            branch_count = int(arg)
    fieldnames = ["Branch Name"]
    fieldnames += list(range(start_timestamp, start_timestamp + period, increment))
    branch_name_list = [randint(1000, 9999) for _ in range(0, branch_count)]
    branch_list = [BranchMetric(branch_name, frequency, start_timestamp, period, increment) for branch_name in branch_name_list]

    with open("branch_metrics.csv", "w", newline="") as metrics_file:
        writer = csv.DictWriter(metrics_file, fieldnames)
        writer.writeheader()
        for branch in branch_list:
            branch.create_metric_array()
            writer.writerow(branch.get_metric_array())


if __name__ == "__main__":
    main(sys.argv[1:])
