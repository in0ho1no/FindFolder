import glob
import os
import tkinter as tk
from enum import Enum, unique
from tkinter import filedialog, messagebox, ttk
from typing import List, Literal


class FolderExplorerApp:
    @unique
    class ColList(Enum):
        DATE = 0
        TYPE = 1
        VER = 2

    COL_DICT_LIST: list[dict] = [
        {  # ColList.DATE
            "ID": "ID_Date",
            "NAME": "Data",
            "ANCHOR": "w",
            "WIDTH": 120,
        },
        {  # ColList.TYPE
            "ID": "ID_Type",
            "NAME": "Type",
            "ANCHOR": "w",
            "WIDTH": 100,
        },
        {  # ColList.VER
            "ID": "ID_Ver",
            "NAME": "Ver",
            "ANCHOR": "w",
            "WIDTH": 60,
        },
    ]

    def __init__(self, root: tk.Tk) -> None:
        """GUI作成"""
        self.root_m = root
        self.root_m.title("FindFolder")

        # ウィンドウのサイズと位置指定
        size_width_def = 400
        size_height_def = 300
        pos_x_def = 10
        pos_y_def = 10
        self.root_m.geometry(f"{size_width_def}x{size_height_def}+{pos_x_def}+{pos_y_def}")

        # 表示するためのframe
        frame = ttk.Frame(self.root_m)
        frame.pack(fill=tk.BOTH, expand=True)

        # フォルダを指定するボタン
        self.btn_folder_open = tk.Button(frame, text="フォルダを開く", command=self.btn_folder_open_click)
        self.btn_folder_open.pack(fill=tk.BOTH, expand=False)

        # フォルダを一覧表示する
        self.treeview_folder = ttk.Treeview(frame)
        self.treeview_folder.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 列名の定義
        self.treeview_folder["columns"] = (
            self.COL_DICT_LIST[self.ColList.DATE.value]["ID"],
            self.COL_DICT_LIST[self.ColList.TYPE.value]["ID"],
            self.COL_DICT_LIST[self.ColList.VER.value]["ID"],
        )

        # 列の定義
        col_num = self.ColList.DATE.value
        self.treeview_folder.column("#0", width=0, stretch=False)  # 不要な0列目を非表示
        self.treeview_folder.column(
            self.COL_DICT_LIST[col_num]["ID"],
            anchor=self.COL_DICT_LIST[col_num]["ANCHOR"],
            width=self.COL_DICT_LIST[col_num]["WIDTH"],
        )
        col_num = self.ColList.TYPE.value
        self.treeview_folder.column(
            self.COL_DICT_LIST[col_num]["ID"],
            anchor=self.COL_DICT_LIST[col_num]["ANCHOR"],
            width=self.COL_DICT_LIST[col_num]["WIDTH"],
        )
        col_num = self.ColList.VER.value
        self.treeview_folder.column(
            self.COL_DICT_LIST[col_num]["ID"],
            anchor=self.COL_DICT_LIST[col_num]["ANCHOR"],
            width=self.COL_DICT_LIST[col_num]["WIDTH"],
        )

        # ヘッダの作成
        col_num = self.ColList.DATE.value
        self.treeview_folder.heading(
            self.COL_DICT_LIST[col_num]["ID"],
            text=self.COL_DICT_LIST[col_num]["NAME"],
            anchor=self.COL_DICT_LIST[col_num]["ANCHOR"],
        )
        col_num = self.ColList.TYPE.value
        self.treeview_folder.heading(
            self.COL_DICT_LIST[col_num]["ID"],
            text=self.COL_DICT_LIST[col_num]["NAME"],
            anchor=self.COL_DICT_LIST[col_num]["ANCHOR"],
        )
        col_num = self.ColList.VER.value
        self.treeview_folder.heading(
            self.COL_DICT_LIST[col_num]["ID"],
            text=self.COL_DICT_LIST[col_num]["NAME"],
            anchor=self.COL_DICT_LIST[col_num]["ANCHOR"],
        )

        # フォルダ一覧にスクロールバーを追加する
        self.scrollbar_list = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.treeview_folder.yview)
        self.scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview_folder.config(yscrollcommand=self.scrollbar_list.set)

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

    def update_folder_listbox(self, folder_path_list_r: list[str]) -> None:
        """フォルダを一覧表示するlistboxの更新

        Args:
            folder_path_list_r (list[str]): フォルダパスのリスト
        """

        # 一覧を全削除する
        for treeview_child in self.treeview_folder.get_children():
            self.treeview_folder.delete(treeview_child)

        # listboxにフォルダパスを設定する
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
