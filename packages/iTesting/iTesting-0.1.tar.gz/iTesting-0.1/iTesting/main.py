# main.py
import argparse


def main():
    parser = argparse.ArgumentParser(prog='iTesting', usage='This is a demo, please follow iTesting on wechat')
    parser.add_argument("name", default='iTesting', help="This is a demo framework", action="store")
    args = parser.parse_args()
    if args.name:
        print("Hello, My name is Kevin Cai, Please search and follow below account from wechat:\n")
        print(args.name)


if __name__ == "__main__":
    main()
