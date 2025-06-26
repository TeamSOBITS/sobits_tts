#!/bin/bash

echo "╔══╣ Install: ParlerTTS Specific Dependencies (STARTING) ╠══╗"

# システムのパッケージリストを更新 (共通スクリプトで実行済みでも、念のため再実行)
sudo apt update -y

echo "--- Installing ParlerTTS Specific Python Dependencies ---"
# 特定バージョンのNumPy (ParlerTTSが特定のバージョンを要求する可能性)
# 共通のsoundfileやpygameでインストールされるnumpyと競合しないよう、
# ここで指定バージョンをインストール。
pip3 install numpy==1.23.5

# 日本語処理用のRubyInserter
pip3 install git+https://github.com/getuka/RubyInserter.git

# ParlerTTS ライブラリ本体の指定バージョン
pip3 install parler_tts==0.2.3

# PyTorch関連のライブラリをアンインストールし、再インストールすることで、
# 環境に最適なバージョンを確実に導入
echo "--- Reinstalling PyTorch and related libraries ---"
pip3 uninstall -y torch torchvision torchaudio
pip3 install torch torchvision torchaudio

# Transformers ライブラリの指定バージョン (ParlerTTSに必要)
pip3 install transformers==4.46.1

# Flash-Attention (高速化用、コメントアウトされているが残す)
# pip3 install flash-attn --no-build-isolation

echo "╚══╣ Install: ParlerTTS Specific Dependencies (FINISHED) ╠══╝"
