"""第1回: Chatに履歴を持たせて連続して質問するスクリプト。

使い方:
    uv run python -m app.chat_ask "LoRAとは何ですか？"
    uv run python -m app.chat_ask            # 質問を省略すると、講座に固有の質問をする

ツールは使わず、Chatの会話履歴を使って連続して質問する。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def chat(first_question: str) -> None:
    with genai.Client(api_key=get_api_key()) as client:
        session = client.chats.create(model=MODEL)  # 履歴はSDKのChatが持つ
        question = first_question
        while question:
            response = session.send_message(question)  # これまでの履歴と今回の質問を送る
            print(response.text or "テキストの回答がありませんでした。")
            usage = response.usage_metadata
            input_tokens = getattr(usage, "prompt_token_count", None)
            output_tokens = getattr(usage, "candidates_token_count", None)
            print(
                f"[tokens] 入力 {input_tokens if input_tokens is not None else '不明'}"
                f" / 出力 {output_tokens if output_tokens is not None else '不明'}"
            )
            question = input("\n[続けて質問 (空行で終了)] ").strip()

def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        chat(args.question)
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()