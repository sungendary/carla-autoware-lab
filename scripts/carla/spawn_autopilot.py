"""Town01 로드 → 차량 1대 스폰 → Traffic Manager 오토파일럿 주행 (동기 모드)."""
import argparse
import math
import random

import carla


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--port", type=int, default=2000)
    ap.add_argument("--tm-port", type=int, default=8000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--duration", type=float, default=60.0)  # 시뮬레이션 시간(초)
    args = ap.parse_args()

    client = carla.Client(args.host, args.port)
    client.set_timeout(30.0)  # 맵 로드는 수 초~수십 초 걸림
    print("client", client.get_client_version(), "/ server", client.get_server_version())

    world = client.load_world("Town01")
    print("map:", world.get_map().name)
    original_settings = world.get_settings()
    tm = client.get_trafficmanager(args.tm_port)
    vehicle = None
    try:
        # 1) 동기 모드: tick() 1회 = 시뮬레이션 0.05초
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)
        tm.set_synchronous_mode(True)
        tm.set_random_device_seed(args.seed)
        random.seed(args.seed)

        # 2) 차량 스폰
        bp = world.get_blueprint_library().find("vehicle.tesla.model3")
        bp.set_attribute("role_name", "hero")
        spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle = world.try_spawn_actor(bp, spawn_point)
        if vehicle is None:
            raise RuntimeError("스폰 실패 (해당 지점에 이미 액터가 있음)")
        start = spawn_point.location
        print(f"spawned id={vehicle.id} at x={start.x:.1f}, y={start.y:.1f}")

        # 3) 오토파일럿 = Traffic Manager에 제어를 맡김
        vehicle.set_autopilot(True, tm.get_port())

        spectator = world.get_spectator()
        steps = int(args.duration / settings.fixed_delta_seconds)
        for i in range(steps):
            world.tick()
            tf = vehicle.get_transform()
            spectator.set_transform(carla.Transform(
                tf.location + carla.Location(z=40), carla.Rotation(pitch=-90)))
            if i % 40 == 0:  # 시뮬레이션 2초마다 출력
                v = vehicle.get_velocity()
                speed = 3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)
                print(f"t={i*0.05:5.1f}s  speed={speed:5.1f} km/h  "
                      f"dist_from_start={tf.location.distance(start):6.1f} m")
    finally:
        # 4) 정리: 스크립트가 죽어도 서버가 멈추지 않게
        if vehicle is not None:
            vehicle.destroy()
        tm.set_synchronous_mode(False)
        world.apply_settings(original_settings)
        print("cleaned up")


if __name__ == "__main__":
    main()