オセロプレイヤーの作成
===

<details>
<summary><h2>準備 (全課題共通)</h2></summary>

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

</details>

## 課題テンプレートのダウンロード

### 課題用レポジトリの作成

講義中に指示する[GitHub Classroom](https://classroom.github.com/classrooms)の課題作成用URLにアクセスし、手順に従うと、課題用のレポジトリである`othello-player-username`が作成される (`username`の部分は各自のGitHubアカウント名に読み替えること)。

### レポジトリのクローン

再び、ローカル環境に戻り、WindowsならコマンドプロンプトかPowerShell, Macならターミナルを開いて、**Gitレポジトリをクローン**する。正しく、SSHの公開鍵が登録されていれば、以下のコマンドでレポジトリがクローンできる。

```shell
# Gitレポジトリのクローン
git clone git@github.com:tatsy-classes/othello-player-username.git
```

### 仮想環境の作成

Anacondaを使って適当な課題用の仮想環境を作成し、その環境にPipを用いて必要なモジュールをインストールする。**GitHub Actions上の自動採点プログラムはPython 3.9を用いている**ので、Anacondaの仮想環境もPython 3.9で作成すること。

```shell
# 仮想環境の作成
conda create -n othello python=3.9
# 仮想環境の切り替え
conda activate othello
# モジュールのインストール
pip install -r requirements.txt
```

## 課題の作成

### ソルバー関数の編集

課題用レポジトリに含まれる `player.py`を編集(**ファイル名は変更しないこと**)して、より強いオセロAIとなるようにプログラムに修正する。編集するべき`MyPlayer`クラスは以下のような定義になっている。

```python
import random

from othello import Env, Move, Player
from players.base import BasePlayer


class MyPlayer(BasePlayer):
    def __init__(self):
        pass

    def reset(self):
        """
        ゲーム開始時に行いたい処理を記述
        """

    def play(self, env: Env) -> Move:
        """
        この関数を主に更新する、以下はランダムに着手する例
        """
        moves = env.legal_moves()
        return random.choice(moves)
```

### ローカルでのテスト方法

`othello.py`が編集できたら、最初にローカル環境でテストを実施する。テストランナには`pytest`を用いるが、今回は対戦相手のスクリプトファイルを`--path`に指定する形でテストを実行する。

```shell
pytest --path players/randomoize.py
```

また、`match.py`を用いると、自分で作成したプレイヤー同士を対戦させることもできる。自分で作成したプレイヤーのスクリプトファイルが`player.py`と`opponent.py`であるとしたとき、以下のコマンドで対戦が実行される。

```shell
python match.py --file1 player.py --file2 opponent.py --n_match 100 --verbose
```

最後の二つの引数`--n_match 100`ならびに`--verbose`の指定は任意だが、前者はテストプレイの回数を、後者は詳細な実行過程を表示するために用いる。

### サーバー上でのテスト方法

`player.py`に行った編集をGitHub上のレポジトリにコミット、プッシュすると、GitHub Actionsの機能を用いて自動採点が実施される。変更をコミット、プッシュするためのコマンドの一例は以下の通り。

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

**注意:** 作成したデータセット等はレポジトリのファイルサイズ制限に引っかかるのでアップロードしないこと。

### 実行時間の制約

テストコードでは各レベルのAIと20回ずつ対戦が行われる。実行時間にはレベル1なら1分、レベル2なら2分、レベル3なら3分の制約が設けられている。それ以上が経過すると、自動的にプログラムが終了するので注意すること。

