"""Irodori TTSのAPIサーバ．

Irodori TTSはtransformers 5系とtorch 2.10系を必要とし，ROS側のPythonと依存関係が衝突するため，
install/irodori.shが作成する専用venvのPythonでこのスクリプトを実行する(irodori_tts.pyが起動する)．
ROSには依存せず，127.0.0.1のみで待ち受ける．

  GET  /health      -> 200 "ok"
  POST /synthesize  -> JSON {text, ref_wav, caption, num_steps, seed} を受け取り, 48kHz の PCM16 WAV を返す
"""
import argparse
import io
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np
import soundfile as sf
import torch


def parse_args():
    parser = argparse.ArgumentParser(description="Irodori-TTS synthesis server")
    parser.add_argument("--irodori-dir", required=True, help="Path to the cloned Irodori-TTS repository")
    parser.add_argument("--checkpoint", default="Aratako/Irodori-TTS-v4.1-Small")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--precision", default="bf16")
    parser.add_argument("--port", type=int, default=50070)
    parser.add_argument("--warmup-ref-wav", default="", help="Reference used for warm-up synthesis")
    parser.add_argument("--warmup-caption", default="")
    parser.add_argument("--warmup-num-steps", type=int, default=16)
    return parser.parse_args()


class IrodoriEngine:
    def __init__(self, args):
        sys.path.insert(0, args.irodori_dir)
        # Irodori既定のcuDNN attentionは初めての長さの入力ごとに計算グラフを作り直すため，
        # 初めての文で1文約1.3秒かかる(同じ文の2回目は約0.3秒)．長さに依らず速いEfficient Attentionを優先する
        from torch.nn.attention import SDPBackend
        import irodori_tts.attention
        irodori_tts.attention._SDPA_PRIORITY = [SDPBackend.EFFICIENT_ATTENTION, SDPBackend.MATH]
        from irodori_tts.inference_runtime import (
            InferenceRuntime, RuntimeKey, SamplingRequest, download_hf_checkpoint)
        self._SamplingRequest = SamplingRequest
        precision = args.precision if args.device.startswith("cuda") else "fp32"
        self.runtime = InferenceRuntime.from_key(RuntimeKey(
            checkpoint=download_hf_checkpoint(args.checkpoint),
            model_device=args.device, codec_device=args.device, model_precision=precision))
        self._latent_cache = {}  # ref_wav のパス -> latent(.pt) のパス
        self._lock = threading.Lock()  # GPU 上の推論は1つずつ行う

    def _ref_latent(self, ref_wav):
        """見本の wav を一度だけ latent に変換し, 以降は使い回す(毎回のエンコードを省く)."""
        key = (ref_wav, os.path.getmtime(ref_wav))
        if key not in self._latent_cache:
            wav, sr = sf.read(ref_wav, dtype="float32", always_2d=True)
            wav = torch.from_numpy(wav.mean(axis=1))[None, None, :].to(self.runtime.codec_device)
            latent = self.runtime.codec.encode_waveform(
                wav, sample_rate=sr, normalize_db=-16.0, ensure_max=True).cpu()
            path = f"/tmp/irodori_ref_{abs(hash(key))}.pt"
            torch.save(latent, path)
            self._latent_cache[key] = path
        return self._latent_cache[key]

    def synthesize(self, text, ref_wav="", caption="", num_steps=16, seed=0):
        with self._lock:
            request = self._SamplingRequest(
                text=text,
                caption=caption or None,
                ref_latent=self._ref_latent(ref_wav) if ref_wav else None,
                no_ref=not ref_wav,
                num_steps=int(num_steps),
                seed=int(seed),
            )
            result = self.runtime.synthesize(request)
        audio = result.audio.float().cpu().numpy().reshape(-1)
        buffer = io.BytesIO()
        sf.write(buffer, np.clip(audio, -1.0, 1.0), result.sample_rate, format="WAV", subtype="PCM_16")
        return buffer.getvalue()


def make_handler(engine):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):  # アクセスログは出さない
            pass

        def _send(self, code, body, content_type):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/health":
                self._send(200, b"ok", "text/plain")
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self):
            if self.path != "/synthesize":
                self._send(404, b"not found", "text/plain")
                return
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                start = time.time()
                wav = engine.synthesize(
                    req["text"], req.get("ref_wav", ""), req.get("caption", ""),
                    req.get("num_steps", 16), req.get("seed", 0))
                print(f"{time.time() - start:.2f}s steps={req.get('num_steps', 16)}: {req['text']}",
                      flush=True)
                self._send(200, wav, "audio/wav")
            except Exception as e:
                print(f"Error: synthesis failed: {e}", flush=True)
                self._send(500, str(e).encode("utf-8"), "text/plain")

    return Handler


def main():
    args = parse_args()
    start = time.time()
    engine = IrodoriEngine(args)
    print(f"model loaded in {time.time() - start:.1f}s", flush=True)

    # 起動直後の数回は GPU の準備で遅いので, 本番の前に空打ちしておく
    if args.warmup_ref_wav:
        for _ in range(3):
            engine.synthesize("ウォームアップです。", args.warmup_ref_wav, args.warmup_caption, args.warmup_num_steps)
        print("warm-up finished", flush=True)

    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(engine))
    print(f"ready on 127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
