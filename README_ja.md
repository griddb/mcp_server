## GridDB向けMCPサーバ

### 概要

GridDB を通じてデータベース操作を提供する Model Context Protocol（MCP）サーバの実装です。このサーバを使用すると、SQL クエリの実行が可能になります。

本ソフトウェアは、MCP Python SDK v1をベースとしています。  
MCPオリジナルのサンプルコードの1つである[SQLite向けMCPサーバ](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite)を流用しています。


### 動作環境

以下の環境で本プログラムの実行を確認しています。

    OS: Windows, Linux
        (Windows) PowerShell
        (Linux) Windows上のWSL, Docker CE
    Python 3.12, uv(パッケージ管理ツール), OpenJDK 21
    MCP Python SDK v1
    GridDB JDBC Driver: V5.9 CE(Community Edition)
    GridDB Server: V5.9 CE, V6.0 EE(Enterprise Edition)

### コンポーネント

#### ツール

このサーバは、参照のみの3つの機能(ツール)を提供します。
- read_query
- list_tables
- describe_table

※ optionalのwrite_query、create_tableを使いたい場合は、src/mcp_server_griddbフォルダ上のserver.pyファイルを
optional/server.pyファイルに差し替えてください。

##### クエリツール

- `read_query`
  - SELECT クエリを実行し、データベースからデータを読み取ります
  - 入力:
    - `query`（文字列）: 実行する SELECT SQL クエリ
  - 戻り値: オブジェクトの配列として返されるクエリ結果

- `write_query` (optional)
  - INSERT、UPDATE、または DELETE クエリを実行します
  - 入力:
    - `query`（文字列）: データを変更する SQL クエリ
  - 戻り値: `{ affected_rows: number }`

- `create_table` (optional)
  - データベースに新しいテーブルを作成します
  - 入力:
    - `query`（文字列）: CREATE TABLE SQL 文
  - 戻り値: テーブル作成の確認結果

##### スキーマツール

- `list_tables`
  - データベース内のすべてのテーブルの一覧を取得します
  - 入力は不要です
  - 戻り値: テーブル名の配列

- `describe_table`
  - 指定したテーブルのスキーマ情報を表示します
  - 入力:
    - `table_name`（文字列）: 説明対象のテーブル名
  - 戻り値: 列名と型を含む列定義の配列

### VS Code での使用方法

2つの方法があります。  
(A) uvを使って、Windows上でMCPサーバを起動する方法  
(B) WSL、Docker CEを使って、Linux上でMCPサーバを起動する方法

#### (A) uv

1. Python、uv、OpenJDKをインストールしてください。
2. 本MCPサーバのソースをユーザ・フォルダに置いてください。例："C:/Users/user1"
3. 以下の JSON ブロックを VS Code の`mcp.json` ファイルに追加してください。`Ctrl + Shift + P` を押し、`MCP: Open User Configuration` と入力するとファイルを開けます。

```json
{
  "servers": {
    "griddb": {
      "command": "uv",
      "args": [
        "run",
        "mcp-server-griddb",
        "--url",
        "(GridDB JDBCドライバのGridDBサーバ接続用URL)",
        "--user",
        "(GridDBユーザ名)",
        "--password",
        "(GridDBユーザ名のパスワード)"
      ],
      "cwd":"(GridDB向けMCPサーバのあるパス)"
    }
  }
}
```

例：
```json
{
  "servers": {
    "griddb": {
      "command": "uv",
      "args": [
        "run",
        "mcp-server-griddb",
        "--url",
        "jdbc:gs://192.0.2.0:20001/myCluster",
        "--user",
        "admin",
        "--password",
        "admin"
      ],
      "cwd":"C:/Users/user1/mcp_server"
    }
  }
}
```

4. PowerShellを起動し、ソースのあるフォルダ(例："C:/Users/user1/mcp_server")に移動し、以下の操作を実行してください。
```
uv sync --frozen --no-install-project --no-dev --no-editable

uv sync --frozen --no-dev --no-editable

curl.exe -L "https://repo1.maven.org/maven2/com/github/griddb/gridstore-jdbc/5.9.0/gridstore-jdbc-5.9.0.jar" -o gridstore-jdbc.jar
```

#### (B) Docker

1. WSL、Docker CEをインストールしてください。
2. 以下の JSON ブロックを VS Code の`mcp.json` ファイルに追加してください。`Ctrl + Shift + P` を押し、`MCP: Open User Configuration` と入力するとファイルを開けます。

```json
{
  "servers": {
    "griddb": {
      "command": "wsl",
      "args": [
        "docker",
        "run",
        "-i",
        "--rm",
        "--network=host",
        "-v",
        "mcp-griddb:/mcp",
        "mcp/griddb",
        "--url",
        "(GridDB JDBCドライバのGridDBサーバ接続用URL)",
        "--user",
        "(GridDBユーザ名)",
        "--password",
        "(GridDBユーザ名のパスワード)"
      ]
    }
  }
}
```

例：
```json
{
  "servers": {
    "griddb": {
      "command": "wsl",
      "args": [
        "docker",
        "run",
        "-i",
        "--rm",
        "--network=host",
        "-v",
        "mcp-griddb:/mcp",
        "mcp/griddb",
        "--url",
        "jdbc:gs://127.0.0.1:20001/myCluster",
        "--user",
        "admin",
        "--password",
        "admin"
      ]
    }
  }
}
```

3. 本MCPサーバのソースをWSL上のフォルダに置いてください。例："\\wsl.localhost\Ubuntu\home\user1"
4. WSLを起動し、ソースのあるフォルダ(例：/home/user1/mcp_server)に移動し、以下の操作でDockerイメージを作成してください。

```bash
docker build -t mcp/griddb .
```

※ VS CodeにおけるMCPサーバの設定を無効化する場合は、`mcp.json` ファイルに追加したJSONブロックを削除してください。


### コミュニティ
  * Issues  
    質問、不具合報告はissue機能をご利用ください。
  * PullRequest  
    GridDB Contributor License Agreement(CLA_rev1.1.pdf)に同意して頂く必要があります。
    PullRequest機能をご利用の場合はGridDB Contributor License Agreementに同意したものとみなします。

### ライセンス

この MCP サーバは MIT License の下でライセンスされています。MIT License の条件に従う限り、このソフトウェアを自由に使用、変更、配布できます。詳細については、プロジェクトリポジトリ内の `LICENSE` ファイルを参照してください。

# 商標

本資料に掲載の会社名もしくは商品名等は、それぞれ各社が商標として使用している場合があります。
