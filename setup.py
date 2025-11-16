"""
初期セットアップスクリプト
デフォルトディレクトリとサンプルファイルを作成
"""
import os
from constants import DATA_DIR, QUESTIONS_DIR, RESPONSES_DIR, LOGS_DIR
from utils import save_questions_to_csv

def create_default_directories():
    """デフォルトディレクトリを作成"""
    directories = [DATA_DIR, QUESTIONS_DIR, RESPONSES_DIR, LOGS_DIR]

    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✓ ディレクトリを作成: {directory}")
            except Exception as e:
                print(f"✗ ディレクトリ作成エラー ({directory}): {e}")
        else:
            print(f"- ディレクトリは既に存在: {directory}")

def create_sample_questions():
    """サンプル問題ファイルを作成"""
    sample_questions = [
        {
            "text": "あなたの好きな季節は何ですか？",
            "choices": ["春", "夏", "秋", "冬"]
        },
        {
            "text": "普段よく使うプログラミング言語は何ですか？",
            "choices": ["Python", "JavaScript", "Java", "C++", "その他"]
        },
        {
            "text": "1日の勉強時間はどのくらいですか？",
            "choices": ["1時間未満", "1〜2時間", "2〜4時間", "4時間以上"]
        }
    ]

    sample_file = os.path.join(QUESTIONS_DIR, "sample_questions.csv")

    if not os.path.exists(sample_file):
        try:
            save_questions_to_csv(sample_questions, sample_file)
            print(f"✓ サンプル問題ファイルを作成: {sample_file}")
        except Exception as e:
            print(f"✗ サンプル問題ファイル作成エラー: {e}")
    else:
        print(f"- サンプル問題ファイルは既に存在: {sample_file}")

def create_readme():
    """data/README.txtを作成"""
    readme_path = os.path.join(DATA_DIR, "README.txt")

    readme_content = """データディレクトリ構造
=====================

このディレクトリには、アンケートアプリケーションのデータが保存されます。

questions/
  - 問題ファイル（CSV/JSON形式）を配置するディレクトリ
  - sample_questions.csv: サンプル問題ファイル

responses/
  - アンケート回答結果が保存されるディレクトリ
  - 形式: responses_{回答者ID}_{日付}.csv または .json

logs/
  - ユーザーアクションログが保存されるディレクトリ
  - 形式: action_log_{回答者ID}_{日付}.csv

設定について
============
- メインメニューの「⚙ 設定」から各ディレクトリとファイル名のフォーマットを変更できます
- デフォルトでこのディレクトリ構造が使用されます
"""

    if not os.path.exists(readme_path):
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print(f"✓ README.txtを作成: {readme_path}")
        except Exception as e:
            print(f"✗ README.txt作成エラー: {e}")
    else:
        print(f"- README.txtは既に存在: {readme_path}")

def setup():
    """セットアップを実行"""
    print("=" * 50)
    print("研究用アンケートシステム - 初期セットアップ")
    print("=" * 50)
    print()

    create_default_directories()
    print()
    create_sample_questions()
    print()
    create_readme()
    print()

    print("=" * 50)
    print("セットアップ完了！")
    print("=" * 50)

if __name__ == "__main__":
    setup()
