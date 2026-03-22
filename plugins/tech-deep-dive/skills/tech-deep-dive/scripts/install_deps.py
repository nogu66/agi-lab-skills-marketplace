#!/usr/bin/env python3
"""
依存モジュール自動インストールスクリプト。

このスクリプトは、tech-research-suiteスキルの実行に必要なPythonパッケージを
自動的にインストールします。

使い方:
  python install_deps.py

出力:
  インストール状況をコンソールに出力します。
"""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """requirements.txt に記載されたパッケージをインストール"""
    script_dir = Path(__file__).parent
    requirements_file = script_dir / 'requirements.txt'

    if not requirements_file.exists():
        print(f"警告: {requirements_file} が見つかりません", file=sys.stderr)
        return False

    print("依存モジュールをインストール中...")
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-q', '-r', str(requirements_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✓ 全ての依存モジュールをインストールしました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"エラー: 依存モジュールのインストールに失敗しました", file=sys.stderr)
        print(f"詳細: {e}", file=sys.stderr)
        return False


if __name__ == '__main__':
    success = install_dependencies()
    sys.exit(0 if success else 1)
