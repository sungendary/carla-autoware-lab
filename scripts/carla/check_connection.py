"""CARLA 서버 접속 확인: RPC(2000) 버전 조회 + 센서 스트리밍(2001) 프레임 수신."""
import argparse
import threading
import time

import carla

p = argparse.ArgumentParser()
p.add_argument("--host", default="carla")
p.add_argument("--port", type=int, default=2000)
p.add_argument("--frames", type=int, default=10)
args = p.parse_args()

client = carla.Client(args.host, args.port)
client.set_timeout(10.0)
print(f"[RPC] client {client.get_client_version()} / server {client.get_server_version()}")

world = client.get_world()
sync = world.get_settings().synchronous_mode
print(f"[RPC] map {world.get_map().name}, synchronous_mode={sync}")

bp = world.get_blueprint_library().find("sensor.camera.rgb")
bp.set_attribute("image_size_x", "320")
bp.set_attribute("image_size_y", "240")
cam = world.spawn_actor(bp, world.get_spectator().get_transform())

frames, done = [], threading.Event()
def on_image(img):
    frames.append(img.frame)
    if len(frames) >= args.frames:
        done.set()

cam.listen(on_image)
try:
    deadline = time.time() + 10
    while not done.is_set() and time.time() < deadline:
        if sync:
            world.tick()          # 동기 모드면 직접 tick해야 센서가 데이터를 보냄
        else:
            time.sleep(0.1)
finally:
    cam.stop()
    cam.destroy()

status = "OK" if done.is_set() else "FAIL (2001 스트리밍 확인 필요)"
print(f"[STREAM] received {len(frames)} frames -> {status}")