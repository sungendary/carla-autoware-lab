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