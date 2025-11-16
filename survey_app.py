"""
研究用アンケートアプリケーション - メインファイル
Googleフォームのようなモダンなデザインのアンケートシステム
"""
import customtkinter as ctk
from tkinter import messagebox
from question_editor import QuestionEditor
from survey_interface import SurveyInterface
from settings_window import SettingsWindow
from config_manager import ConfigManager
from constants import (
    MAIN_WINDOW_SIZE, FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_SUBTITLE,
    COLOR_GRAY, COLOR_GRAY_HOVER
)
import os

# 初期セットアップを実行（ディレクトリが存在しない場合のみ）
from constants import DATA_DIR
if not os.path.exists(DATA_DIR):
    from setup import setup
    setup()

# 設定を読み込んで外観を適用
config_manager = ConfigManager()
appearance_mode = config_manager.get("appearance_mode", "System")
color_theme = config_manager.get("color_theme", "blue")

ctk.set_appearance_mode(appearance_mode)
ctk.set_default_color_theme(color_theme)


class SurveyApp:
    """メインアプリケーションクラス"""

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("研究用アンケートシステム")
        self.root.geometry(MAIN_WINDOW_SIZE)

        self._setup_ui()

    def _setup_ui(self):
        """UIをセットアップ"""
        # メインフレーム
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # タイトル
        title_label = ctk.CTkLabel(
            main_frame,
            text="研究用アンケートシステム",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold")
        )
        title_label.pack(pady=40)

        # ボタンフレーム
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=40)

        # ボタンを作成
        self._create_buttons(button_frame)

    def _create_buttons(self, parent):
        """ボタンを作成"""
        buttons = [
            ("問題を作成", self.open_question_editor, None, None),
            ("アンケートに回答", self.open_survey_interface, None, None),
            ("⚙ 設定", self.open_settings, "gray50", "gray40"),
            ("終了", self.root.quit, COLOR_GRAY, COLOR_GRAY_HOVER)
        ]

        for text, command, fg_color, hover_color in buttons:
            btn_args = {
                "text": text,
                "command": command,
                "font": (FONT_FAMILY, FONT_SIZE_SUBTITLE),
                "width": 300,
                "height": 50
            }

            if fg_color and hover_color:
                btn_args["fg_color"] = fg_color
                btn_args["hover_color"] = hover_color

            btn = ctk.CTkButton(parent, **btn_args)
            btn.pack(pady=15)

    def open_question_editor(self):
        """問題作成エディタを開く"""
        editor_window = ctk.CTkToplevel(self.root)
        QuestionEditor(editor_window)

    def open_survey_interface(self):
        """アンケート回答画面を開く"""
        survey_window = ctk.CTkToplevel(self.root)
        SurveyInterface(survey_window)

    def open_settings(self):
        """設定画面を開く"""
        settings_window = ctk.CTkToplevel(self.root)
        SettingsWindow(settings_window)

    def run(self):
        """アプリケーションを実行"""
        self.root.mainloop()


if __name__ == "__main__":
    app = SurveyApp()
    app.run()
