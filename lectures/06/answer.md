# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前： glossary_search_glossary
- STEP 2 の [tool call]： glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]： fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]： aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要', 'topics': ['general']})
                          aws_aws___search_documentation({'search_phrase': 'What is S3 Versioning Amazon Simple Storage Service', 'topics': ['general']})            
- 気づき・疑問：
 glossaryサーバーと公開サーバーfetchでは、回答生成にツールは1回のみ使われた。awsのMCPサーバーでは、最初に質問のキーワードがsearch_documentationツールで使われ、次に質問文章が英訳されたテキストがsearch_documentationツールで使われた。

 | MCPサーバー名  |     入力     |    出力    | モデル応答  |
 |---------------|--------------|-----------|------------|
 |glossaryサーバー| 715 tokens   | 143 tokens |    2回     |
 |fetchサーバー   | 2179 tokens  | 118 tokens |    2回     |
 | awsサーバー　　| 11367 tokens |  145 tokens |   3 回    |
 外部サーバーを使った場合は自作のMCPサーバーを使う場合と比較して、入力トークン数が増加すること、モデル応答回数も増えることがある。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 

- やったこと：新しいツールget_lecture_summaryを、MCPサーバーglossaryで公開した。

- 結果：「第2回では何を学びますか？」と質問した。結果として、get_lecture_summaryが呼ばれて、以下の出力が得られた。
[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
[model] gemini-3.5-flash-lite
[tools] MCP サーバー（app/mcp_servers.json）
第2回では、「**ファインチューニングとLoRA**」について学びます。
　### 主な学習内容
　1. **事前学習とファインチューニングの違い**
   　- 汎用的な能力を身につける「事前学習」と、目的のタスクに適応させる「ファインチューニング」の役割や、向く場面・向かない場面を理解します。
　2. **SFT（教師あり微調整）**
   　- 入力と望ましい出力のペアを用いて、モデルの出力形式や口調などを整える方法を学びます。
　3. **PEFTとLoRA**
   　- 全パラメータを更新するのではなく、小さな低ランク行列を追加して学習コストを大幅に削減する「LoRA」の仕組みとハイパーパラメータ（ランク $r$、学習率、エポック数など）を学びます。
　4. **QLoRAとの関係や過学習への注意**
   - 4bit量子化とLoRAを組み合わせたQLoRAの考え方や、過学習（オーバーフィッティング）への注意点についても触れます。
　### 演習
　　- Google Colab上で小さなモデル（Qwen2.5など）を架空のFAQデータでLoRA学習させ、学習の前後で出力の質がどのように変わるかを実際に体験します。
　（関連回：第2回）　　
　--- trace ---
　[tool call]   glossary_get_lecture_summary({'lecture': 2})
　[tool return] glossary_get_lecture_summary -> # 第2回 ファインチューニングとLoRA
　　## この回のねらい
　　　　- 事前学習とファインチューニングの違い、ファインチューニングが向く場面と向かない場面を理解する
　　　　- LoRAの考え方を理解し、Google Colab上で小さなモデルを…
　[usage] 入力 5,942 tokens / 出力 315 tokens / モデル応答 2 回

- 気づき・疑問：
　エージェントは、起動すると毎回公開されているツール一覧をサーバーに問い合わせるので、mcp_agent.pyに新しいツールを追加せずに、mcp_server.pyに新しいツールを追加すれば、エージェントは新しいツールを使えることを確認できた。

- 取り組んだレベル：実装

- やったこと：第３回で作ったツール(make_quiz)を、app.mcp_server.pyで公開しました。引数が範囲外の時に、分かりやすいメッセージを返すように実装した。

- 結果：「第2回の内容から確認問題を出してください」と入力した。結果として、make_quizが呼ばれて、以下の出力が得られた。
 [server] glossary: コマンドで起動（uv run python -m app.mcp_server）
 [server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
 [server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
 [model] gemini-3.5-flash-lite
 [tools] MCP サーバー（app/mcp_servers.json）
 それでは、第2回の内容から確認問題を1問出題します！
 **【確認問題】**
 事前学習済みモデルを、特定のタスクや形式に合ったデータで追加学習させ、出力の形式や口調、特定ドメインの振る舞いを身につけさせる手法を何と呼ぶでしょうか？
 （ヒント：最新の事実を覚えさせる用途にはRAGなどが向いていますが、出力形式や専門的な口調を適応させたいときによく使われるアプローチです。）
 答えがわかったら教えてくださいね！
（関係する回：第2回）
 --- trace ---
 [tool call]   glossary_make_quiz({'lecture': 2})
 [tool return] glossary_make_quiz -> {"question": "次の用語の定義は何でしょうか？: ファインチューニング", "answer": "事前学習済みモデルを、特定のタスクや形式に合ったデータで追加学習させること。出力の形式や口調、特定ドメインの振る舞いを身につけさせ…
 [usage] 入力 5,685 tokens / 出力 147 tokens / モデル応答 2 回

- 結果：「第99回のクイズを出してください」と入力した。結果として、make_quizが呼ばれて、以下の出力が得られた。
　[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
　[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
　[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
　[model] gemini-3.5-flash-lite
　[tools] MCP サーバー（app/mcp_servers.json）
　申し訳ありませんが、第99回という回は講座の範囲外（または存在しない回）のため、確認問題を作成することができません。
　講座の通常の回（第1回〜など）の確認問題や、学習したい特定の用語がありましたら、該当する回や用語名を教えていただければ喜んでサポートいたします！
　--- trace ---
　[usage] 入力 2,777 tokens / 出力 68 tokens / モデル応答 1 回

- 気づき・疑問：第99回という範囲外のコメントに対して、ツールmake_quizは、"第99回の用語は用意されていません。"と返答させた。この返答に対して、LLMが "申し訳ありませんが、第99回という回は講座の範囲外（または存在しない回）のため、確認問題を作成することができません。講座の通常の回（第1回〜など）の確認問題や、学習したい特定の用語がありましたら、該当する回や用語名を教えていただければ喜んでサポートいたします！"と、丁寧な回答を生成した。