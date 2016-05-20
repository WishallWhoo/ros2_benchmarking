#!/usr/bin/python3

import os, sys, argparse, subprocess
from TestRunner import TestRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    testing= parser.add_argument_group('testing', '')
    testing.add_argument("--loss", type=int, nargs='+', help="run loss tests for given values [%%]")
    testing.add_argument("--delay", type=int, nargs='+', help="run delay tests for given values [ms]")
    testing.add_argument("--limit", type=int, nargs='+', help="run limit tests for given values [kbit]")
    testing.add_argument("--duplication", type=int, nargs='+', help="run duplication tests for given values [%%]")
    testing.add_argument("--corruption", type=int, nargs='+', help="run corruption tests for given values [%%]")
    testing.add_argument("--reorder", type=int, nargs='+', help="run reorder tests for given values [%%]")
    testing.add_argument("--skip-ros1", action='store_true', help="skip ros1 tests")
    testing.add_argument("--skip-ros2", action='store_true', help="skip ros2 tests")
    tools = parser.add_argument_group('tools', '')
    tools.add_argument("--build-all", action='store_true', help ="build all images")
    tools.add_argument("--build", help = "delete an existing image and build a new one", choices = ["ros1", "ros1node", "ros2", "ros2node"])
    tools.add_argument("--replot", action='store_true', help ="plot again current results")
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")
    elif len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.build:
            subprocess.call("./scripts/build_container.sh {}".format(args.build), shell = True)
        elif args.build_all:
            for name in [ 'ros1', 'ros1node', 'ros2', 'ros2node' ]:
                subprocess.call("./scripts/build_container.sh {}".format(name), shell = True)
        elif args.replot:
            subprocess.call("sh ./graphs/replot.sh", shell = True)
        else:
            runner = TestRunner()
            runner.clean()
            comms = []
            if not args.skip_ros1:
                comms.append("ros1")
            if not args.skip_ros2:
                comms.append("ros2")
            for comm in comms:
                if args.limit:
                    runner.limit(comm, args.limit)
                if args.duplication:
                    runner.duplication(comm, args.duplication)
                if args.corruption:
                    runner.corruption(comm, args.corruption)
                if args.reorder:
                    runner.reorder(comm, args.reorder)
                if args.loss:
                    runner.loss(comm, args.loss)
                if args.delay:
                    runner.delay(comm, args.delay)
            runner.clean()