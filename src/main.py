import glob
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class FolderExplorerApp:
    def __init__(self, root: tk.Tk) -> None:
        """GUI作成"""
        self.root_m = root
        self.root_m.title("FindFolder")

        # ウィンドウのサイズと位置指定
        size_width_def = 300
        size_height_def = 100
        pos_x_def = 10
        pos_y_def = 10
        self.root_m.geometry(f"{size_width_def}x{size_height_def}+{pos_x_def}+{pos_y_def}")

        # Frame for Listbox
        frame = ttk.Frame(self.root_m)
        frame.pack(fill=tk.BOTH, expand=True)

        # フォルダを指定するボタン
        self.btn_folder_open = tk.Button(frame, text="フォルダを開く", command=self.btn_folder_open_click)
        self.btn_folder_open.pack(fill=tk.BOTH, expand=True)

        # フォルダを一覧表示するlistbox
        self.listbox_folder = tk.Listbox(frame, selectmode=tk.SINGLE)
        self.listbox_folder.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # listboxにスクロールバーを追加する
        self.scrollbar_list = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox_folder.yview)
        self.scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_folder.config(yscrollcommand=self.scrollbar_list.set)

    def open_folder(self) -> list[str]:
        """対象とするフォルダを選択する

        Returns:
            list[str]: 指定されたフォルダに含まれるフォルダ一覧
        """

        # ユーザにフォルダ選択を促す
        folder_path = filedialog.askdirectory(title="検索対象フォルダを選択してください")
        if os.path.isdir(folder_path) is False:
            messagebox.showerror("エラー", "フォルダが存在しません。")
            return []

        # 指定されたフォルダ内のフォルダ一覧を取得する
        folder_path_list = glob.glob(f"{folder_path}\\**\\")
        if 0 == len(folder_path_list):
            messagebox.showerror("エラー", "フォルダの中身が空です。")
            return []

        return folder_path_list

    def update_folder_listbox(self, folder_path_list_r: list[str]) -> None:
        """フォルダを一覧表示するlistboxの更新

        Args:
            folder_path_list_r (list[str]): フォルダパスのリスト
        """

        # listboxをクリアする
        self.listbox_folder.delete(0, tk.END)

        # listboxにフォルダパスを設定する
        for folder_path in folder_path_list_r:
            self.listbox_folder.insert(tk.END, folder_path)

    def btn_folder_open_click(self) -> None:
        """指定フォルダ内のフォルダ一覧を表示する"""
        folder_path_list = self.open_folder()
        self.update_folder_listbox(folder_path_list)


def main() -> None:
    root = tk.Tk()
    FolderExplorerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
