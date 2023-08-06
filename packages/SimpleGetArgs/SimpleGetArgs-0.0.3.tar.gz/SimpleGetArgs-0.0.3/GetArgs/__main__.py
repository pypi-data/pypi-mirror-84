import argparse
# import sys, os
import sys
import os

# PACKAGE_PARENT = '..'
# SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from .ManagingArgs.Adding_Simple import AddSimple
from .ManagingArgs.Adding_Simple import AddSimple
from .ManagingArgs.Criteria import ArgsCriteria

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--counttill100', required=False, action='store_true', help='Print count till 100')
    parser.add_argument('--print1', required=False, action='store_true', help='Let you to Print Hello to any name')
    parser.add_argument('--name', type=str, default='Farnoush', help='Print Name')

    return parser


def main(argv=None):
    """
    :desc: Entry point method
    """
    if argv is None:
        argv = sys.argv

    try:
        parser = create_parser()
        args = parser.parse_args(argv[1:])

        # Arguments initialization
        counttill100 = args.counttill100
        name = args.name
        print1 = args.print1


        # Parser check
        if counttill100:
            print(AddSimple().print_till100())
            # counttill100fun()

        if print1:
            print(AddSimple().sayhello(name))


    except KeyboardInterrupt:
        print('\nGood Bye.')

    return 0

def counttill100fun():
    for i in range(1, 101):
        print(i)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

