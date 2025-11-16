"""
定数定義ファイル
アプリケーション全体で使用する定数を一元管理
"""
import os

# ========================================
# ディレクトリ構造
# ========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
QUESTIONS_DIR = os.path.join(DATA_DIR, "questions")
RESPONSES_DIR = os.path.join(DATA_DIR, "responses")
LOGS_DIR = os.path.join(DATA_DIR, "logs")

# ========================================
# ファイル名
# ========================================
CONFIG_FILE = "config.json"
DEFAULT_QUESTIONS_FILE = "sample_questions.csv"

# ========================================
# UI設定
# ========================================
# ウィンドウサイズ
MAIN_WINDOW_SIZE = "900x700"
EDITOR_WINDOW_SIZE = "1000x750"
SETTINGS_WINDOW_SIZE = "800x650"
SURVEY_WINDOW_SIZE = "900x800"

# フォント
FONT_FAMILY = "Yu Gothic"
FONT_SIZE_TITLE = 28
FONT_SIZE_SECTION = 24
FONT_SIZE_SUBTITLE = 16
FONT_SIZE_NORMAL = 14
FONT_SIZE_BUTTON = 14
FONT_SIZE_LABEL = 12
FONT_SIZE_SMALL = 11
FONT_SIZE_TINY = 10

# 色設定
COLOR_SELECTED = ["#2CC985", "#2FA572"]  # 選択された選択肢（緑）
COLOR_SELECTED_HOVER = ["#27B372", "#2B965F"]
COLOR_DEFAULT = ["#3B8ED0", "#1F6AA5"]  # デフォルトボタン（青）
COLOR_DEFAULT_HOVER = ["#36719F", "#144870"]
COLOR_GRAY = "gray40"
COLOR_GRAY_HOVER = "gray30"
COLOR_LIGHT_GRAY = "gray70"
COLOR_DARK_GRAY = "gray30"

# ========================================
# ログ設定
# ========================================
LOG_ACTIONS = {
    "CHOICE_SELECTION": "選択肢選択",
    "REASON_START": "理由入力開始",
    "REASON_TEXT": "理由入力内容",
    "REASON_REWRITE": "理由書き直し",
    "QUESTION_MOVE": "問題移動",
    "SUBMIT": "アンケート送信"
}

# ログのテキストプレビュー文字数
LOG_TEXT_PREVIEW_LENGTH = 100

# ========================================
# バリデーション設定
# ========================================
MIN_CHOICES = 2  # 最低選択肢数
MAX_CHOICES = 10  # 最大選択肢数
DEFAULT_CHOICES = 2  # デフォルト選択肢数

# ========================================
# ファイル名フォーマット変数
# ========================================
FILENAME_VARIABLES = {
    "date": "日付(YYYYMMDD)",
    "time": "時刻(HHMMSS)",
    "respondent_id": "回答者ID",
    "sequence": "連番"
}

# ========================================
# デフォルト設定値
# ========================================
DEFAULT_CONFIG = {
    "questions_directory": QUESTIONS_DIR,
    "questions_file": DEFAULT_QUESTIONS_FILE,
    "log_directory": LOGS_DIR,
    "log_name_format": "action_log_{respondent_id}_{date}.csv",
    "response_directory": RESPONSES_DIR,
    "response_name_format": "responses_{respondent_id}_{date}.csv",
    "appearance_mode": "System",
    "color_theme": "blue",
    "output_format": "csv",
    "font_size": "medium",
    "auto_save": True
}

# ========================================
# メッセージ
# ========================================
MSG_NO_QUESTIONS = "保存する問題がありません"
MSG_NO_QUESTION_TEXT = "質問文を入力してください"
MSG_MIN_CHOICES = f"最低{MIN_CHOICES}つの選択肢を入力してください"
MSG_QUESTION_ADDED = "問題を追加しました"
MSG_NO_CHOICE_SELECTED = "選択肢を選んでください"
MSG_NO_REASON = "理由を記入してください"
MSG_CANNOT_CHANGE_CHOICE = "理由を書き始めた後は選択肢を変更できません。\n「理由を書き直す」ボタンを押してください。"
MSG_CHANGE_DISABLED_STATUS = "⚠ 理由を書き直してから選択肢を変更してください"
MSG_REASON_STARTED_STATUS = "理由を書き直すまで選択肢は変更できません"
MSG_CAN_CHANGE_STATUS = "選択肢を変更できます"
