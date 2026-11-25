"""CARLA 월드 상태 확인: 맵, 동기 모드(fixed_delta_seconds), 차량 액터(role_name·위치), 센서 수.

용도: Autoware 재시작 사이에 CARLA 동기 모드가 남았는지, ego·센서 액터가 잔류했는지 확인한다(#15).
읽기만 하고 tick이나 설정 변경은 하지 않는다.

Autoware 정지 중에만 실행: e2e 실행 중에는 인터페이스가 tick을 관리하므로 다른 클라이언트 접속을 피한다(env.md 규칙).
"""
import argparse
import carla

p = argparse.ArgumentParser()
p.add_argument("--host", default="localhost")
p.add_argument("--port", type=int, default=2000)
a = p.parse_args()

c = carla.Client(a.host, a.port)
c.set_timeout(10.0)
w = c.get_world()
s = w.get_settings()
print("map:", w.get_map().name)
print("synchronous_mode:", s.synchronous_mode, "fixed_delta_seconds:", s.fixed_delta_seconds)
for v in w.get_actors().filter("vehicle.*"):
    loc = v.get_transform().location
    print("vehicle", v.id, v.type_id, v.attributes.get("role_name"), round(loc.x, 2), round(loc.y, 2))
print("sensors:", len(w.get_actors().filter("sensor.*")))