"""
設定管理モジュール
"""
import json
import os
from datetime import datetime
from constants import DEFAULT_CONFIG, CONFIG_FILE


class ConfigManager:
    """設定を管理するクラス"""

    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """設定を読み込む"""
        # デフォルト設定を定数からコピー
        default_config = DEFAULT_CONFIG.copy()

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # デフォルト設定とマージ
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"設定ファイルの読み込みエラー: {e}")

        return default_config

    def save_config(self):
        """設定を保存"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"設定ファイルの保存エラー: {e}")
            return False

    def get(self, key, default=None):
        """設定値を取得"""
        return self.config.get(key, default)

    def set(self, key, value):
        """設定値を設定"""
        self.config[key] = value

    def get_questions_path(self):
        """問題ファイルのパスを取得"""
        questions_dir = self.get("questions_directory", "")
        questions_file = self.get("questions_file", "")

        if questions_dir and questions_file:
            return os.path.join(questions_dir, questions_file)
        return None

    def get_log_path(self, respondent_id=None):
        """ログファイルのパスを取得"""
        log_dir = self.get("log_directory", "")
        log_name_format = self.get("log_name_format", "action_log_{date}.csv")

        if not log_dir:
            log_dir = "."

        # フォーマット文字列を置換
        now = datetime.now()
        filename = log_name_format.replace("{date}", now.strftime("%Y%m%d"))
        filename = filename.replace("{time}", now.strftime("%H%M%S"))
        if respondent_id:
            filename = filename.replace("{respondent_id}", respondent_id)

        # 連番を処理
        if "{sequence}" in filename:
            from utils import get_next_sequence_number
            seq_num = get_next_sequence_number(log_dir, filename)
            filename = filename.replace("{sequence}", str(seq_num).zfill(3))

        return os.path.join(log_dir, filename)

    def get_response_path(self, respondent_id):
        """回答ファイルのパスを取得"""
        response_dir = self.get("response_directory", "")
        response_name_format = self.get("response_name_format", "responses_{respondent_id}_{date}.csv")

        if not response_dir:
            response_dir = "."

        # フォーマット文字列を置換
        now = datetime.now()
        filename = response_name_format.replace("{date}", now.strftime("%Y%m%d"))
        filename = filename.replace("{time}", now.strftime("%H%M%S"))
        filename = filename.replace("{respondent_id}", respondent_id)

        # 連番を処理
        if "{sequence}" in filename:
            from utils import get_next_sequence_number
            seq_num = get_next_sequence_number(response_dir, filename)
            filename = filename.replace("{sequence}", str(seq_num).zfill(3))

        return os.path.join(response_dir, filename)

    def ensure_directories(self):
        """必要なディレクトリを作成"""
        dirs = [
            self.get("questions_directory"),
            self.get("log_directory"),
            self.get("response_directory")
        ]

        for directory in dirs:
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except Exception as e:
                    print(f"ディレクトリ作成エラー: {e}")
