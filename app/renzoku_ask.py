"""会話履歴を保持し、続けて質問できるスクリプト。"""

import argparse

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat, question: str) -> str:
    # 同じchatを使うと、過去の質問・回答を含めて送信される
    response = chat.send_message(question)

    usage = response.usage_metadata
    input_tokens = getattr(usage, "prompt_token_count", None)
    output_tokens = getattr(usage, "candidates_token_count", None)

    print(
        f"[トークン数] 入力: "
        f"{input_tokens if input_tokens is not None else '不明'}, "
        f"出力: "
        f"{output_tokens if output_tokens is not None else '不明'}"
    )

    return response.text or "テキストの回答がありませんでした。"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="会話履歴を保持しながらLLMに質問する"
    )
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print("続けて質問できます。終了するには exit または 終了 と入力してください。\n")

    # クライアントとチャットは、会話の開始時に一度だけ作成する
    with genai.Client(api_key=get_api_key()) as client:
        chat = client.chats.create(
            model=MODEL,
            config=types.GenerateContentConfig(
                temperature=1.0,
            ),
        )

        question = args.question

        while True:
            print(f"[質問] {question}\n")

            try:
                answer = ask(chat, question)
                print(f"[回答]\n{answer}\n")
            except errors.APIError as e:
                print(api_error_message(e.code, e.message))
                print("質問を入力し直してください。\n")

            # 次の質問を受け付ける。空入力の場合は再入力する
            while True:
                question = input("次の質問 > ").strip()

                if question.lower() in {"exit", "quit", "終了"}:
                    print("会話を終了します。")
                    return

                if question:
                    break

                print("質問を入力してください。")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n会話を終了します。")