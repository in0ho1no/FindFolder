# FindFolder

## 開発

### テンプレートから作成後に実行する

workspace名の変更

    git mv wsXXX.code-workspace wsFindFolder.code-workspace

README.mdのタイトルを変更する

### 環境準備

仮想環境を作成する

    pipenv --python 3.10

pyinstallerの用意

    pipenv install pyinstaller

### ビルド

    pyinstaller ./src/main.py --onefile --clean --name FindFolder
