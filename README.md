オセロプレイヤーの作成
===

## 準備 (全課題共通)

### GitHubのアカウントを作成

<https://github.com/>にアクセスしてアカウントを作成する。

### Gitクライアントのインストール (Windows向け)

Windowsの場合にはGitが最初からインストールされていないので、

- [Git for Windows](https://gitforwindows.org/)

を各自のコンピュータにインストールする。インストール後、コマンドプロンプトかPowerShellを実行して、

- `git`
- `ssh-keygen`

の2つのコマンドが認識されるかどうかを確認する。認識されない場合にはWindowsを再起動する。

### Gitクライアントのインストール (Mac向け)

Macの場合は工場出荷時時点で既にGitがインストールされている。ターミナルを開いて

- `git`
- `ssh-keygen`

の2つのコマンドが認識されるかどうかを確認する。

### SSHキーの登録

現在、GitHubはSSHの認証鍵を使わないとプライベートレポジトリをダウンロードできないので、SSHキーをGitHubアカウントに登録する。

Windows/Macともに、以下のコマンドで4096ビット長のRSA鍵を作成する。

```shell
# SSHキーペア(秘密鍵と公開鍵)の作成。以下のコマンドは4096bit長のRSA暗号を用いる
ssh-keygen -t rsa -b 4096
```

途中、パスワードの入力などを求められるが、特に不要なら入力する必要はない。

コマンドが正しく実行されると、ホームディレクトリの`.ssh`ディレクトリ内に`id_rsa`と`id_rsa.pub`の二つのファイルが生成される。この二つのうち、`id_rsa`の方は秘密鍵、`id_rsa.pub`の方は公開鍵のファイルである。サーバーに登録して良いのは公開鍵の方だけなので注意すること。

公開鍵のファイル`id_rsa.pub`を何らかのエディタで開いて、その内容をコピーする。GitHubに移動し、右上のユーザアイコンをクリックし「Settings」を選ぶ。その後、「SSH and GPG keys」を左のメニューから選び、「SSH Keys」の右にある「New SSH key」ボタンを押して、現れるテキストボックスに先ほど`id_rsa.pub`からコピーした内容を貼り付けて、「Add SSH key」を押す。

## 課題テンプレートのダウンロード

### 課題用レポジトリの作成

講義中に指示する課題作成用URLにアクセスし、手順に従うと、課題用のレポジトリである`ogura-agent-username`が作成される (`username`の部分は各自のGitHubアカウント名に読み替えること)。

### レポジトリのクローン

再び、ローカル環境に戻り、WindowsならコマンドプロンプトかPowerShell, Macならターミナルを開いて、Gitレポジトリをクローンする。正しく、SSHの公開鍵が登録されていれば、以下のコマンドでレポジトリがクローンされる。

```shell
# Gitレポジトリのクローン
git clone git@github.com:tatsy-classes/ogura-agent-username.git
```

### 仮想環境の作成

Anacondaを使って適当な課題用の仮想環境を作成し、その環境にPipを用いて必要なモジュールをインストールする。GitHub Actions上の自動採点プログラムはPython 3.9を用いているので、Anacondaの仮想環境もPython 3.9で作成すること。

```shell
# 仮想環境の作成
conda create -n ogura python=3.9
# 仮想環境の切り替え
conda activate ogura
# モジュールのインストール
pip install -r requirements.txt
```

## 課題の作成

### ソルバー関数の編集

課題用レポジトリ (本レポジトリ)に含まれる `ogura.py`を編集(**ファイル名は変更しないこと**)して、課題の目的が達成されるようなプログラムに修正する。編集するべき`solve`関数は以下のような定義になっている。

```python
def solve(image: NDArray[np.uint8], poems: List[str], level: int) -> List[int]:
    """
    Inputs:
      image: input image
      poems: list of ogura poems
      level: difficulty level of this problem (1-3)
    Outputs:
      answer: list of determination status
        0: specific poem does not exist in the image
        1: possible poem can exist in the image, but there remains other possible poems
        2: the specific poem exist in the card, and there is no other possible poems
    """
    answer = [0] * len(poems)
    return answer
```

### ローカルでのテスト方法

`ogura.py`が編集できたら、最初にローカル環境でテストを実施する。`data`ディレクトリの中に1枚ずつサンプルの画像が入っているのでそれを利用してよい。

また、講義の参加者には`data/samples.zip`の展開用パスワードを指示するので、このZIPファイルに含まれる各レベル5枚のサンプル画像も合わせて使用すること。ZIPファイルを展開すると`level1`から`level3`のフォルダが得られるので、これを`data/level1`から`data/level3`にそれぞれ上書きする。

準備ができたら、`pytest`を使ってテストを実行する。

```shell
# 汎用的なテスト
pytest 
# 実行状況を細かく表示する場合
pytest --tb=long
```

### サーバー上でのテスト方法

`ogura.py`に行った編集をGitHub上のレポジトリにコミット、プッシュすると、GitHub Actionsの機能を用いて自動採点が実施される。変更をコミット、プッシュするためのコマンドの一例は以下の通り。

```shell
# リポジトリのルートディレクトリで以下を実行する
# -----
## ローカルの更新状況を確認
git status -u
## ローカルの変更をGitの履歴に反映
git add -u
## 必要に応じて自分で作成したファイルも追加
git add "/file/name/you/wanna/track"
## コミット
git commit -m "コミットコメント (適宜更新内容を入力)"
## プッシュ
git push origin master
```

**注意:** 作成したデータセットはレポジトリのファイルサイズ制限に引っかかるのでアップロードしないこと。

### 実行時間の制約

実行時間は1問当たり最大1分とする。それ以上が経過すると、自動的にプログラムが終了するので注意すること。

