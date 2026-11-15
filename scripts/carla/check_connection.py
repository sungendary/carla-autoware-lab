"""CARLA 서버 접속 확인: RPC(2000) 버전 조회 + 센서 스트리밍(2001) 프레임 수신."""
import argparse
import sys
import threading
import time

import carla

p = argparse.ArgumentParser()
p.add_argument("--host", default="carla")
p.add_argument("--port", type=int, default=2000)
p.add_argument("--frames", type=int, default=10)
p.add_argument("--tick", action="store_true",
               help="동기 모드일 때 이 스크립트가 직접 world.tick() (tick하는 다른 클라이언트가 없을 때만)")
args = p.parse_args()

client = carla.Client(args.host, args.port)
client.set_timeout(10.0)
print(f"[RPC] client {client.get_client_version()} / server {client.get_server_version()}")

world = client.get_world()
sync = world.get_settings().synchronous_mode
do_tick = sync and args.tick   # 비동기 모드면 --tick은 무시
print(f"[RPC] map {world.get_map().name}, synchronous_mode={sync}, tick={do_tick}")

frames, done = [], threading.Event()
def on_image(img):
    frames.append(img.frame)
    if len(frames) >= args.frames:
        done.set()

cam = None
try:
    bp = world.get_blueprint_library().find("sensor.camera.rgb")
    bp.set_attribute("image_size_x", "320")
    bp.set_attribute("image_size_y", "240")
    cam = world.spawn_actor(bp, world.get_spectator().get_transform())
    cam.listen(on_image)
    deadline = time.time() + 10
    while not done.is_set() and time.time() < deadline:
        if do_tick:
            world.tick()          # 동기 모드에서는 tick해야 센서가 데이터를 보냄
        else:
            time.sleep(0.1)       # 비동기 모드, 또는 다른 클라이언트가 tick한다고 가정
finally:
    if cam is not None:
        cam.stop()
        cam.destroy()

if done.is_set():
    print(f"[STREAM] received {len(frames)} frames -> OK")
else:
    if sync and not do_tick:
        reason = "동기 모드인데 tick하는 클라이언트가 없음 → --tick 사용"
    else:
        reason = "2001 스트리밍 확인 필요"
    print(f"[STREAM] received {len(frames)} frames -> FAIL ({reason})")
    sys.exit(1)
