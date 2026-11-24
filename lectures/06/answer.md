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

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
