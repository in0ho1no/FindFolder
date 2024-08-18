import glob
import os
import tkinter as tk
from enum import Enum, unique
from tkinter import filedialog, messagebox, ttk


class FolderExplorerApp:
    """GUI作成"""

    class FolderTreeview:
        """フォルダを一覧表示するTreeview"""

        @unique
        class ColList(Enum):
            DATE = 0
            TYPE = 1
            VER = 2

        COL_REVERSE_DEFAULT = False
        COL_DICT_LIST: list[dict] = [
            {  # ColList.DATE
                "ID": "ID_Date",
                "NAME": "Data",
                "ANCHOR": "w",
                "WIDTH": 120,
                "REVERSE": COL_REVERSE_DEFAULT,
            },
            {  # ColList.TYPE
                "ID": "ID_Type",
                "NAME": "Type",
                "ANCHOR": "w",
                "WIDTH": 100,
                "REVERSE": COL_REVERSE_DEFAULT,
            },
            {  # ColList.VER
                "ID": "ID_Ver",
                "NAME": "Ver",
                "ANCHOR": "w",
                "WIDTH": 60,
                "REVERSE": COL_REVERSE_DEFAULT,
            },
        ]

        def __init__(self, frame_r: ttk.Frame) -> None:
            self.frame_m = frame_r

            # フォルダを一覧表示する
            self.treeview_folder = ttk.Treeview(self.frame_m)
            self.treeview_folder.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # 列名の定義
            self.treeview_folder["columns"] = (
                self.COL_DICT_LIST[self.ColList.DATE.value]["ID"],
                self.COL_DICT_LIST[self.ColList.TYPE.value]["ID"],
                self.COL_DICT_LIST[self.ColList.VER.value]["ID"],
            )

            # 列の定義
            self.treeview_folder.column("#0", width=0, stretch=False)  # 不要な0列目を非表示

            self.treeview_folder.column(
                self.COL_DICT_LIST[self.ColList.DATE.value]["ID"],
                anchor=self.COL_DICT_LIST[self.ColList.DATE.value]["ANCHOR"],
                width=self.COL_DICT_LIST[self.ColList.DATE.value]["WIDTH"],
            )
            self.treeview_folder.column(
                self.COL_DICT_LIST[self.ColList.TYPE.value]["ID"],
                anchor=self.COL_DICT_LIST[self.ColList.TYPE.value]["ANCHOR"],
                width=self.COL_DICT_LIST[self.ColList.TYPE.value]["WIDTH"],
            )
            self.treeview_folder.column(
                self.COL_DICT_LIST[self.ColList.VER.value]["ID"],
                anchor=self.COL_DICT_LIST[self.ColList.VER.value]["ANCHOR"],
                width=self.COL_DICT_LIST[self.ColList.VER.value]["WIDTH"],
            )

            # ヘッダの作成
            self.treeview_folder.heading(
                self.COL_DICT_LIST[self.ColList.DATE.value]["ID"],
                text=self.COL_DICT_LIST[self.ColList.DATE.value]["NAME"],
                anchor=self.COL_DICT_LIST[self.ColList.DATE.value]["ANCHOR"],
                command=lambda: self.treeview_header_click(self.ColList.DATE.value),
            )
            self.treeview_folder.heading(
                self.COL_DICT_LIST[self.ColList.TYPE.value]["ID"],
                text=self.COL_DICT_LIST[self.ColList.TYPE.value]["NAME"],
                anchor=self.COL_DICT_LIST[self.ColList.TYPE.value]["ANCHOR"],
                command=lambda: self.treeview_header_click(self.ColList.TYPE.value),
            )
            self.treeview_folder.heading(
                self.COL_DICT_LIST[self.ColList.VER.value]["ID"],
                text=self.COL_DICT_LIST[self.ColList.VER.value]["NAME"],
                anchor=self.COL_DICT_LIST[self.ColList.VER.value]["ANCHOR"],
                command=lambda: self.treeview_header_click(self.ColList.VER.value),
            )

            # フォルダ一覧にスクロールバーを追加する
            scrollbar_list = tk.Scrollbar(self.frame_m, orient=tk.VERTICAL, command=self.treeview_folder.yview)
            scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
            self.treeview_folder.config(yscrollcommand=scrollbar_list.set)

        def update_folder_list(self, folder_path_list_r: list[str]) -> None:
            """フォルダ一覧の更新

            Args:
                folder_path_list_r (list[str]): フォルダパスのリスト
            """

            # 一覧を全削除する
            for treeview_child in self.treeview_folder.get_children():
                self.treeview_folder.delete(treeview_child)

            # 並び替え指定を初期化する
            for col_dict in self.COL_DICT_LIST:
                col_dict["REVERSE"] = self.COL_REVERSE_DEFAULT

            # フォルダパスをパースして表示する
            for folder_path in folder_path_list_r:
                dir_name = folder_path.split(os.sep)[-2]
                date, type, var = dir_name.split("_")
                self.treeview_folder.insert(
                    parent="",
                    index="end",
                    values=(
                        date,
                        type,
                        var,
                    ),
                )

            # 初回の並び替えを行う
            self.sort_column(self.ColList.DATE.value)

        def sort_column(self, col_num_r: int) -> None:
            """指定された列に応じてリストを並び替える"""

            # リストの要素取得
            folder_list = self.treeview_folder.get_children()
            if 0 == len(folder_list):
                return

            # リストの並び替え
            data_list = [(self.treeview_folder.set(folder, self.COL_DICT_LIST[col_num_r]["ID"]), folder) for folder in folder_list]
            data_list.sort(reverse=self.COL_DICT_LIST[col_num_r]["REVERSE"])
            for index, (_, item) in enumerate(data_list):
                self.treeview_folder.move(item, "", index)

            # 次回に向けて並び替え指定を更新
            self.COL_DICT_LIST[col_num_r]["REVERSE"] = not self.COL_DICT_LIST[col_num_r]["REVERSE"]

        def treeview_header_click(self, col_num_r: int) -> None:
            """ヘッダクリック時のイベントを行う

            Args:
                col_num_r (int): クリックされた列番号
            """
            self.sort_column(col_num_r)

    def __init__(self, root: tk.Tk) -> None:
        self.root_m = root
        self.root_m.title("FindFolder")

        # ウィンドウのサイズと位置指定
        size_width_def = 400
        size_height_def = 300
        pos_x_def = 10
        pos_y_def = 10
        self.root_m.geometry(f"{size_width_def}x{size_height_def}+{pos_x_def}+{pos_y_def}")

        # 表示するためのframe
        self.frame_m = ttk.Frame(self.root_m)
        self.frame_m.pack(fill=tk.BOTH, expand=True)

        # フォルダを指定するボタン
        self.btn_folder_open_m = tk.Button(self.frame_m, text="フォルダを開く", command=self.btn_folder_open_click)
        self.btn_folder_open_m.pack(fill=tk.BOTH, expand=False)

        # フォルダ一覧を表示する
        self.folder_treeview_m = self.FolderTreeview(self.frame_m)

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
        folder_path_list = glob.glob(f"{folder_path}{os.sep}**{os.sep}")
        if 0 == len(folder_path_list):
            messagebox.showerror("エラー", "フォルダの中身が空です。")
            return []

        return folder_path_list

    def btn_folder_open_click(self) -> None:
        """指定フォルダ内のフォルダ一覧を表示する"""
        folder_path_list = self.open_folder()
        self.folder_treeview_m.update_folder_list(folder_path_list)


def main() -> None:
    root = tk.Tk()
    FolderExplorerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
