"""
ユーティリティ関数 - CSV入出力など
"""
import csv
import json
import os
from datetime import datetime


def save_questions_to_csv(questions, filepath):
    """
    質問リストをCSVファイルに保存

    Args:
        questions: 質問データのリスト
        filepath: 保存先ファイルパス
    """
    try:
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)

            # ヘッダー
            writer.writerow(['問題番号', '質問文', '選択肢1', '選択肢2', '選択肢3', '選択肢4', '選択肢5'])

            # 各質問を書き込み
            for i, question in enumerate(questions, 1):
                row = [i, question['text']]
                row.extend(question['choices'])

                # 選択肢が5つに満たない場合は空文字で埋める
                while len(row) < 7:
                    row.append('')

                writer.writerow(row)

        return True
    except Exception as e:
        print(f"CSV保存エラー: {e}")
        return False


def save_questions_to_json(questions, filepath):
    """
    質問リストをJSONファイルに保存

    Args:
        questions: 質問データのリスト
        filepath: 保存先ファイルパス
    """
    try:
        data = {
            "questions": questions,
            "total_questions": len(questions),
            "created_date": get_timestamp()
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"JSON保存エラー: {e}")
        return False


def load_questions_from_csv(filepath):
    """
    CSVファイルから質問リストを読み込み

    Args:
        filepath: 読み込むファイルパス

    Returns:
        質問データのリスト
    """
    questions = []

    try:
        if not os.path.exists(filepath):
            return questions

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)

            # ヘッダーをスキップ
            next(reader, None)

            for row in reader:
                if len(row) < 2:
                    continue

                question = {
                    'text': row[1],
                    'choices': [choice for choice in row[2:] if choice.strip()]
                }

                questions.append(question)

        return questions
    except Exception as e:
        print(f"CSV読み込みエラー: {e}")
        return questions


def load_questions_from_json(filepath):
    """
    JSONファイルから質問リストを読み込み

    Args:
        filepath: 読み込むファイルパス

    Returns:
        質問データのリスト
    """
    questions = []

    try:
        if not os.path.exists(filepath):
            return questions

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # データ形式のバリデーション
            if isinstance(data, list):
                questions = data
            elif isinstance(data, dict) and 'questions' in data:
                questions = data['questions']

        return questions
    except Exception as e:
        print(f"JSON読み込みエラー: {e}")
        return questions


def load_questions(filepath):
    """
    ファイルから質問リストを読み込み（拡張子に応じてCSVまたはJSON）

    Args:
        filepath: 読み込むファイルパス

    Returns:
        質問データのリスト
    """
    if filepath.endswith('.json'):
        return load_questions_from_json(filepath)
    else:
        return load_questions_from_csv(filepath)


def save_response_to_csv(responses, filepath):
    """
    回答データをCSVファイルに保存

    Args:
        responses: 回答データのリスト
        filepath: 保存先ファイルパス
    """
    try:
        file_exists = os.path.exists(filepath)

        with open(filepath, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)

            # ファイルが新規の場合はヘッダーを書き込む
            if not file_exists:
                writer.writerow(['回答者ID', 'タイムスタンプ', '問題番号', '質問文', '選択した回答', '理由'])

            # 回答を書き込み
            for response in responses:
                writer.writerow([
                    response['respondent_id'],
                    response['timestamp'],
                    response['question_num'],
                    response['question_text'],
                    response['selected_choice'],
                    response['reason']
                ])

        return True
    except Exception as e:
        print(f"回答保存エラー: {e}")
        return False


def get_timestamp():
    """現在のタイムスタンプを取得"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def get_next_sequence_number(directory, base_filename):
    """
    指定されたディレクトリで次の連番を取得

    Args:
        directory: ディレクトリパス
        base_filename: ベースとなるファイル名（{sequence}を含む）

    Returns:
        次の連番
    """
    if not directory or not os.path.exists(directory):
        return 1

    # {sequence}を.*に置き換えてパターンを作成
    import re
    pattern = base_filename.replace("{sequence}", r"(\d+)")
    pattern = pattern.replace(".", r"\.")
    pattern = pattern.replace("{date}", r"\d{8}")
    pattern = pattern.replace("{time}", r"\d{6}")
    pattern = pattern.replace("{respondent_id}", r"[^_]+")

    max_num = 0
    try:
        for filename in os.listdir(directory):
            match = re.search(pattern, filename)
            if match:
                try:
                    num = int(match.group(1))
                    max_num = max(max_num, num)
                except (ValueError, IndexError):
                    pass
    except Exception as e:
        print(f"連番取得エラー: {e}")

    return max_num + 1


def save_response_to_json(responses, filepath):
    """
    回答データをJSONファイルに保存

    Args:
        responses: 回答データのリスト
        filepath: 保存先ファイルパス
    """
    try:
        data = {
            "responses": responses,
            "export_date": get_timestamp(),
            "total_responses": len(responses)
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"JSON保存エラー: {e}")
        return False


def save_response(responses, filepath, output_format="csv"):
    """
    回答データを指定された形式で保存

    Args:
        responses: 回答データのリスト
        filepath: 保存先ファイルパス（拡張子なし）
        output_format: 出力形式 ("csv", "json", "both")
    """
    success = True

    if output_format in ["csv", "both"]:
        csv_path = filepath if filepath.endswith(".csv") else f"{filepath}.csv"
        if not save_response_to_csv(responses, csv_path):
            success = False

    if output_format in ["json", "both"]:
        json_path = filepath.replace(".csv", ".json") if filepath.endswith(".csv") else f"{filepath}.json"
        if not save_response_to_json(responses, json_path):
            success = False

    return success
