"""
タイムスタンプロガー - ボタン操作のログを記録
"""
import csv
import os
from datetime import datetime
from constants import LOG_ACTIONS, LOG_TEXT_PREVIEW_LENGTH


class ActionLogger:
    """ユーザーアクションをログに記録するクラス"""

    def __init__(self, log_file="action_log.csv"):
        self.log_file = log_file
        self.initialize_log_file()

    def initialize_log_file(self):
        """ログファイルを初期化"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['タイムスタンプ', 'アクション種別', '詳細情報'])

    def log_action(self, action_type, details=""):
        """
        アクションをログに記録

        Args:
            action_type: アクションの種類（例: "選択肢クリック", "理由入力開始"）
            details: 詳細情報
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        try:
            with open(self.log_file, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, action_type, details])
        except Exception as e:
            print(f"ログ記録エラー: {e}")

    def log_choice_selection(self, question_num, choice):
        """選択肢の選択をログに記録"""
        self.log_action(
            LOG_ACTIONS["CHOICE_SELECTION"],
            f"問題{question_num}: {choice}"
        )

    def log_reason_start(self, question_num):
        """理由入力開始をログに記録"""
        self.log_action(
            LOG_ACTIONS["REASON_START"],
            f"問題{question_num}"
        )

    def log_reason_text(self, question_num, reason_text):
        """理由のテキスト内容をログに記録"""
        # テキストが長い場合は最初のLOG_TEXT_PREVIEW_LENGTH文字のみ記録
        max_len = LOG_TEXT_PREVIEW_LENGTH
        preview = reason_text[:max_len] + "..." if len(reason_text) > max_len else reason_text
        self.log_action(
            LOG_ACTIONS["REASON_TEXT"],
            f"問題{question_num}: {preview}"
        )

    def log_rewrite_reason(self, question_num):
        """理由の書き直しをログに記録"""
        self.log_action(
            LOG_ACTIONS["REASON_REWRITE"],
            f"問題{question_num}"
        )

    def log_next_question(self, from_num, to_num):
        """次の問題への移動をログに記録"""
        self.log_action(
            LOG_ACTIONS["QUESTION_MOVE"],
            f"問題{from_num} → 問題{to_num}"
        )

    def log_submit(self):
        """アンケート送信をログに記録"""
        self.log_action(LOG_ACTIONS["SUBMIT"], "完了")
