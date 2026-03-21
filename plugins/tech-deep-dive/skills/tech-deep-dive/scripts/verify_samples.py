#!/usr/bin/env python3
"""
コードサンプルと実装ガイドの検証スクリプト。

使い方:
  # samples/ ディレクトリのコードサンプルを検証
  python verify_samples.py samples/

  # 実装ガイドのコードブロックを抽出して検証
  python verify_samples.py --extract-md implementation_guide.md

  # 環境変数エラーを無視（デフォルト: 有効）
  python verify_samples.py --no-ignore-env samples/

出力:
  各サンプルの実行結果をJSON形式で標準出力に出力する。
  検証レポートを verification_report.md として出力先ディレクトリに生成する。
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# 環境変数未設定を示すエラーパターン
ENV_ERROR_PATTERNS = [
    r"(?i)api.?key",
    r"(?i)api.?token",
    r"(?i)secret",
    r"(?i)credential",
    r"(?i)auth.?token",
    r"(?i)access.?key",
    r"(?i)OPENAI",
    r"(?i)ANTHROPIC",
    r"(?i)GOOGLE",
    r"(?i)AWS_",
    r"(?i)AZURE",
    r"(?i)HF_TOKEN",
    r"(?i)HUGGING",
    r"(?i)environment variable",
    r"(?i)env var",
    r"(?i)not set",
    r"(?i)missing.*key",
    r"(?i)KeyError.*KEY",
    r"(?i)ValueError.*key",
    r"(?i)AuthenticationError",
    r"(?i)PermissionError.*token",
]


def is_env_error(stderr: str, returncode: int) -> bool:
    """環境変数未設定に起因するエラーかどうかを判定する。"""
    if returncode == 0:
        return False
    combined = stderr
    for pattern in ENV_ERROR_PATTERNS:
        if re.search(pattern, combined):
            return True
    return False


def detect_language(filepath: Path) -> str | None:
    """ファイル拡張子から言語を判定する。"""
    ext_map = {
        ".py": "python",
        ".ts": "typescript",
        ".js": "javascript",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".sh": "bash",
    }
    return ext_map.get(filepath.suffix)


def find_main_file(sample_dir: Path) -> Path | None:
    """サンプルディレクトリからメインファイルを検出する。"""
    # main.* を優先
    for f in sample_dir.iterdir():
        if f.stem == "main" and f.suffix in (".py", ".ts", ".js", ".go", ".rs", ".rb"):
            return f
    # index.* を次に検索
    for f in sample_dir.iterdir():
        if f.stem == "index" and f.suffix in (".py", ".ts", ".js", ".go", ".rs", ".rb"):
            return f
    # 単一のソースファイル
    source_files = [
        f
        for f in sample_dir.iterdir()
        if f.suffix in (".py", ".ts", ".js", ".go", ".rs", ".rb")
    ]
    if len(source_files) == 1:
        return source_files[0]
    return None


def install_deps(sample_dir: Path) -> dict:
    """依存関係をインストールする。"""
    result = {"installed": False, "method": None, "output": "", "error": ""}

    req_file = sample_dir / "requirements.txt"
    pkg_json = sample_dir / "package.json"

    if req_file.exists():
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file), "-q"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        result["installed"] = proc.returncode == 0
        result["method"] = "pip"
        result["output"] = proc.stdout
        result["error"] = proc.stderr
    elif pkg_json.exists():
        proc = subprocess.run(
            ["npm", "install", "--silent"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(sample_dir),
        )
        result["installed"] = proc.returncode == 0
        result["method"] = "npm"
        result["output"] = proc.stdout
        result["error"] = proc.stderr
    else:
        result["installed"] = True
        result["method"] = "none"

    return result


def run_file(filepath: Path, cwd: Path, timeout: int = 60) -> dict:
    """ファイルを実行して結果を返す。"""
    lang = detect_language(filepath)
    if not lang:
        return {
            "success": False,
            "error": f"未対応の拡張子: {filepath.suffix}",
            "stdout": "",
            "stderr": "",
            "returncode": -1,
        }

    cmd_map = {
        "python": [sys.executable, str(filepath)],
        "typescript": ["npx", "tsx", str(filepath)],
        "javascript": ["node", str(filepath)],
        "go": ["go", "run", str(filepath)],
        "rust": ["cargo", "run"],
        "ruby": ["ruby", str(filepath)],
        "bash": ["bash", str(filepath)],
    }

    cmd = cmd_map.get(lang)
    if not cmd:
        return {
            "success": False,
            "error": f"実行コマンド未定義: {lang}",
            "stdout": "",
            "stderr": "",
            "returncode": -1,
        }

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd),
        )
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout[:2000],
            "stderr": proc.stderr[:2000],
            "returncode": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"タイムアウト ({timeout}秒)",
            "stdout": "",
            "stderr": "",
            "returncode": -1,
        }
    except FileNotFoundError as e:
        return {
            "success": False,
            "error": f"コマンド未検出: {e}",
            "stdout": "",
            "stderr": "",
            "returncode": -1,
        }


def extract_code_blocks(md_path: Path) -> list[dict]:
    """Markdownファイルからコードブロックを抽出する。"""
    content = md_path.read_text(encoding="utf-8")
    # ```言語名 で始まるコードブロックを抽出
    pattern = r"```(python|typescript|javascript|js|ts|go|bash|sh)\n(.*?)```"
    blocks = []
    for match in re.finditer(pattern, content, re.DOTALL):
        lang = match.group(1)
        code = match.group(2).strip()
        # インストールコマンドのみのブロックはスキップ
        if code.startswith("pip install") or code.startswith("npm install"):
            continue
        # 短すぎるブロック（1行以下）はスキップ
        if len(code.splitlines()) <= 1:
            continue
        # コマンド実行例（$ で始まる行のみ）はスキップ
        lines = code.splitlines()
        if all(line.strip().startswith("$") or line.strip() == "" for line in lines):
            continue
        # 言語名を正規化
        lang_normalize = {"js": "javascript", "ts": "typescript", "sh": "bash"}
        lang = lang_normalize.get(lang, lang)

        ext_map = {
            "python": ".py",
            "typescript": ".ts",
            "javascript": ".js",
            "go": ".go",
            "bash": ".sh",
        }
        blocks.append(
            {"lang": lang, "code": code, "ext": ext_map.get(lang, ".txt"), "line": content[: match.start()].count("\n") + 1}
        )
    return blocks


def verify_samples_dir(samples_dir: Path, ignore_env: bool) -> list[dict]:
    """samples/ ディレクトリの各サンプルを検証する。"""
    results = []
    for sample_dir in sorted(samples_dir.iterdir()):
        if not sample_dir.is_dir():
            continue

        entry = {
            "name": sample_dir.name,
            "path": str(sample_dir),
            "deps": None,
            "execution": None,
            "status": "unknown",
        }

        # 依存関係のインストール
        deps_result = install_deps(sample_dir)
        entry["deps"] = deps_result

        if not deps_result["installed"]:
            entry["status"] = "deps_failed"
            results.append(entry)
            continue

        # メインファイルの検出と実行
        main_file = find_main_file(sample_dir)
        if not main_file:
            entry["status"] = "no_main_file"
            entry["execution"] = {"error": "メインファイルが見つからない"}
            results.append(entry)
            continue

        exec_result = run_file(main_file, sample_dir)
        entry["execution"] = exec_result

        if exec_result["success"]:
            entry["status"] = "pass"
        elif ignore_env and is_env_error(exec_result.get("stderr", ""), exec_result.get("returncode", -1)):
            entry["status"] = "env_skip"
        else:
            entry["status"] = "fail"

        results.append(entry)
    return results


def verify_md_blocks(md_path: Path, ignore_env: bool) -> list[dict]:
    """Markdownファイルのコードブロックを検証する。"""
    blocks = extract_code_blocks(md_path)
    results = []

    for i, block in enumerate(blocks):
        entry = {
            "index": i + 1,
            "lang": block["lang"],
            "line": block["line"],
            "code_preview": block["code"][:100] + ("..." if len(block["code"]) > 100 else ""),
            "status": "unknown",
        }

        # 一時ファイルに書き出して実行
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = Path(tmpdir) / f"block_{i}{block['ext']}"
            tmpfile.write_text(block["code"], encoding="utf-8")

            exec_result = run_file(tmpfile, Path(tmpdir))
            entry["execution"] = exec_result

            if exec_result["success"]:
                entry["status"] = "pass"
            elif ignore_env and is_env_error(exec_result.get("stderr", ""), exec_result.get("returncode", -1)):
                entry["status"] = "env_skip"
            else:
                entry["status"] = "fail"

        results.append(entry)
    return results


def generate_report(sample_results: list[dict], md_results: list[dict], output_path: Path):
    """検証レポートをMarkdownで生成する。"""
    lines = ["# 検証レポート", ""]

    if sample_results:
        lines.append("## コードサンプル検証結果")
        lines.append("")
        lines.append("| サンプル | ステータス | 詳細 |")
        lines.append("|---|---|---|")
        for r in sample_results:
            status_map = {
                "pass": "成功",
                "fail": "失敗",
                "env_skip": "環境変数エラー（無視）",
                "deps_failed": "依存関係エラー",
                "no_main_file": "メインファイル未検出",
            }
            status = status_map.get(r["status"], r["status"])
            detail = ""
            if r["status"] == "fail" and r.get("execution"):
                detail = r["execution"].get("stderr", "")[:80]
            elif r["status"] == "no_main_file":
                detail = "main.* ファイルが見つからない"
            lines.append(f"| {r['name']} | {status} | {detail} |")
        lines.append("")

    if md_results:
        lines.append("## 実装ガイド コードブロック検証結果")
        lines.append("")
        lines.append("| # | 言語 | 行番号 | ステータス | 詳細 |")
        lines.append("|---|---|---|---|---|")
        for r in md_results:
            status_map = {
                "pass": "成功",
                "fail": "失敗",
                "env_skip": "環境変数エラー（無視）",
            }
            status = status_map.get(r["status"], r["status"])
            detail = ""
            if r["status"] == "fail" and r.get("execution"):
                detail = r["execution"].get("stderr", "")[:80]
            lines.append(f"| {r['index']} | {r['lang']} | L{r['line']} | {status} | {detail} |")
        lines.append("")

    # サマリー
    all_results = sample_results + md_results
    total = len(all_results)
    passed = sum(1 for r in all_results if r["status"] == "pass")
    env_skip = sum(1 for r in all_results if r["status"] == "env_skip")
    failed = sum(1 for r in all_results if r["status"] == "fail")
    other = total - passed - env_skip - failed

    lines.append("## サマリー")
    lines.append("")
    lines.append(f"- 合計: {total}")
    lines.append(f"- 成功: {passed}")
    lines.append(f"- 環境変数エラー（無視）: {env_skip}")
    lines.append(f"- 失敗: {failed}")
    if other > 0:
        lines.append(f"- その他: {other}")

    report_content = "\n".join(lines) + "\n"
    output_path.write_text(report_content, encoding="utf-8")
    return report_content


def main():
    parser = argparse.ArgumentParser(description="コードサンプル・実装ガイドの検証")
    parser.add_argument("target", help="samples/ ディレクトリ または Markdownファイルのパス")
    parser.add_argument("--extract-md", action="store_true", help="Markdownからコードブロックを抽出して検証")
    parser.add_argument("--no-ignore-env", action="store_true", help="環境変数エラーを無視しない")
    parser.add_argument("--report", default=None, help="検証レポートの出力先パス")
    parser.add_argument("--json", action="store_true", help="JSON形式で結果を出力")
    args = parser.parse_args()

    ignore_env = not args.no_ignore_env
    target = Path(args.target)

    sample_results = []
    md_results = []

    if args.extract_md or target.suffix == ".md":
        if not target.is_file():
            print(f"エラー: ファイルが見つからない: {target}", file=sys.stderr)
            sys.exit(1)
        md_results = verify_md_blocks(target, ignore_env)
    else:
        if not target.is_dir():
            print(f"エラー: ディレクトリが見つからない: {target}", file=sys.stderr)
            sys.exit(1)
        sample_results = verify_samples_dir(target, ignore_env)

    # レポート生成
    report_path = Path(args.report) if args.report else target.parent / "verification_report.md"
    report = generate_report(sample_results, md_results, report_path)

    if args.json:
        output = {
            "samples": sample_results,
            "md_blocks": md_results,
            "report_path": str(report_path),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(report)

    # 失敗があれば終了コード1
    all_results = sample_results + md_results
    if any(r["status"] == "fail" for r in all_results):
        sys.exit(1)


if __name__ == "__main__":
    main()
