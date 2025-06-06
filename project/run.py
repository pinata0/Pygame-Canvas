# run.py

import os
import sys
import main

def get_user_confirmation():
    while True:
        user_input = input('quadtree 시각화를 수행하시겠습니까? (Y/N) : ').strip().lower()
        if user_input in ['y', 'Y']:
            return True
        elif user_input in ['n', 'N']:
            return False
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    current_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(current_path)
    os.chdir(base_dir)

    is_debug = get_user_confirmation()
    main.main(is_debug)
