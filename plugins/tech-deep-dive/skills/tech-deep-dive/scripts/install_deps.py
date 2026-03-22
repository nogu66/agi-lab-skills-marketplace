#!/usr/bin/env python3
"""
依存モジュール自動インストールスクリプト。

このスクリプトは、tech-deep-diveスキルの実行に必要な
PythonパッケージとNode.jsパッケージを自動的にインストールします。

使い方:
  python install_deps.py

出力:
  インストール状況をコンソールに出力します。
"""

import subprocess
import sys
from pathlib import Path
import shutil


def install_python_dependencies():
    """requirements.txt に記載されたパッケージをインストール"""
    script_dir = Path(__file__).parent
    requirements_file = script_dir / 'requirements.txt'

    if not requirements_file.exists():
        print(f"警告: {requirements_file} が見つかりません", file=sys.stderr)
        return False

    print("Python依存モジュールをインストール中...")
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-q', '-r', str(requirements_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✓ Python依存モジュールをインストールしました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"エラー: Python依存モジュールのインストールに失敗しました", file=sys.stderr)
        print(f"詳細: {e}", file=sys.stderr)
        return False


def install_node_dependencies():
    """package.json に記載されたパッケージをインストール"""
    script_dir = Path(__file__).parent
    package_file = script_dir / 'package.json'

    if not package_file.exists():
        print(f"警告: {package_file} が見つかりません", file=sys.stderr)
        return False

    # npm が利用可能か確認
    if not shutil.which('npm'):
        print("警告: npm が見つかりません。Node.js依存関係のインストールをスキップします")
        print("      Node.js と npm をインストールしてから再実行してください")
        return False

    print("Node.js依存モジュールをインストール中...")
    try:
        # まずローカルの node_modules をクリーンアップ
        node_modules = script_dir / 'node_modules'
        if node_modules.exists():
            import shutil as sh
            sh.rmtree(node_modules, ignore_errors=True)

        # npm install を実行
        subprocess.check_call(
            ['npm', 'install', '--prefix', str(script_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✓ Node.js依存モジュールをインストールしました")

        # インストール確認
        modules_to_check = ['playwright', 'pptxgenjs']
        missing = []
        for mod in modules_to_check:
            mod_path = script_dir / 'node_modules' / mod
            if not mod_path.exists():
                missing.append(mod)

        if missing:
            print(f"警告: {', '.join(missing)} がインストールされていません", file=sys.stderr)
            return False

        return True
    except subprocess.CalledProcessError as e:
        print(f"エラー: Node.js依存モジュールのインストールに失敗しました", file=sys.stderr)
        print(f"詳細: {e.stderr.decode() if hasattr(e, 'stderr') else e}", file=sys.stderr)
        return False


if __name__ == '__main__':
    print("tech-deep-dive スキルの依存モジュール自動インストール")
    print("=" * 50)

    py_success = install_python_dependencies()
    node_success = install_node_dependencies()

    print("=" * 50)
    if py_success and node_success:
        print("✓ すべての依存モジュールの準備が完了しました")
        sys.exit(0)
    else:
        print("⚠ 一部の依存モジュール導入に問題があります")
        sys.exit(1)
