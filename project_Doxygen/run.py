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
    """
    프로그램 실행 진입점입니다.

    - 현재 파일의 경로를 기준으로 프로젝트 루트 디렉토리로 이동한 후,
    - main.py의 main() 함수를 호출하여 애플리케이션을 실행합니다.
    
    이렇게 하면 경로 문제 없이 리소스 파일이나 상대 경로가 일관되게 유지됩니다.
    """
    current_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(current_path)
    os.chdir(base_dir)

    is_debug = get_user_confirmation()
    main.main(is_debug)
