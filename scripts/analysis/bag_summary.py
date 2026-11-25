"""rosbag 주행 요약: AUTO~ARRIVED(없으면 bag 끝) 구간의 시간·출발 지연·속도·NVTL·정지·정지 원인·goal 오차."""
import math
import sys
from collections import Counter

from rclpy.serialization import deserialize_message
from rosbag2_py import ConverterOptions, SequentialReader, StorageOptions
from rosidl_runtime_py.utilities import get_message

NVTL_TOPIC = "/localization/pose_estimator/nearest_voxel_transformation_likelihood"
PF_PREFIX = "/planning/planning_factors/"
NVTL_MIN_OK = 2.3      # NDT 수렴 기준 (env.md #14)
STOP_SPEED = 0.1       # m/s 미만이면 정지로 봄
STOP_MIN_SEC = 1.0     # 이 시간 이상 정지하면 '중간 정지'로 기록


def main():
    bag = sys.argv[1]
    goal = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) >= 4 else None

    reader = SequentialReader()
    reader.open(StorageOptions(uri=bag, storage_id="sqlite3"), ConverterOptions("cdr", "cdr"))
    types = {t.name: get_message(t.type) for t in reader.get_all_topics_and_types()}

    nvtl, speed = [], []
    cmd = []                # (t, 명령 속도, 명령 가속도)
    behaviors = Counter()   # velocity_factors (behavior, status) 건수
    pfactors = Counter()    # planning_factors (모듈, behavior, detail) 건수
    t_auto = t_arrived = last_pos = None
    t_last = None
    while reader.has_next():
        topic, data, t_ns = reader.read_next()
        t = t_ns * 1e-9                      # bag 기록 시각(wall). RTF≈1이라 sim 시간과 거의 같음
        t_last = t
        msg = deserialize_message(data, types[topic])
        if topic == NVTL_TOPIC:
            nvtl.append((t, msg.data))
        elif topic == "/localization/kinematic_state":
            speed.append((t, msg.twist.twist.linear.x))
            last_pos = msg.pose.pose.position
        elif topic == "/control/command/control_cmd":
            cmd.append((t, msg.longitudinal.velocity, msg.longitudinal.acceleration))
        elif topic == "/api/operation_mode/state" and msg.mode == 2 and t_auto is None:
            t_auto = t
        elif topic == "/api/routing/state" and msg.state == 3 and t_arrived is None:
            t_arrived = t
        elif topic == "/api/planning/velocity_factors" and t_auto is not None:
            for f in msg.factors:
                behaviors[(f.behavior, f.status)] += 1   # status 1 APPROACHING, 2 STOPPED
        elif topic.startswith(PF_PREFIX) and t_auto is not None:
            module = topic[len(PF_PREFIX):]
            for f in msg.factors:
                pfactors[(module, f.behavior, f.detail)] += 1

    if t_auto is None:
        print("AUTO(mode 2) 전환이 bag에 없음 → 구간을 정할 수 없음")
        return
    arrived = t_arrived is not None
    t_end = t_arrived if arrived else t_last

    in_run = lambda s: [(t, v) for t, v in s if t_auto <= t <= t_end]
    run_speed, run_nvtl = in_run(speed), in_run(nvtl)
    t_move = next((t for t, v in run_speed if v >= STOP_SPEED), None)   # AUTO 후 처음 움직인 시각

    # 출발 후 처음 움직인 뒤 STOP_MIN_SEC 이상 멈춘 구간 (끝까지 멈춘 경우 포함)
    stops, moved, stop_start = [], False, None
    for t, v in run_speed:
        if v >= STOP_SPEED:
            moved = True
            if stop_start is not None and t - stop_start >= STOP_MIN_SEC:
                stops.append((stop_start - t_auto, t - stop_start, False))
            stop_start = None
        elif moved and stop_start is None:
            stop_start = t
    if stop_start is not None and not arrived and t_end - stop_start >= STOP_MIN_SEC:
        stops.append((stop_start - t_auto, t_end - stop_start, True))

    vals = [v for _, v in run_nvtl]
    label = "AUTO→ARRIVED" if arrived else "AUTO→bag 끝 (도착 안 함)"
    print(f"주행 시간 {label}: {t_end - t_auto:.1f} s")
    if t_move is not None:
        print(f"출발 지연 AUTO→첫 이동: {t_move - t_auto:.1f} s, 이동 시간 첫 이동→끝: {t_end - t_move:.1f} s")
        # 출발 지연 구간에 Autoware가 보낸 명령: 0이면 Autoware가 출발을 늦춤, >0이면 차가 명령을 못 따름
        run_cmd = [(t, v, a) for t, v, a in cmd if t_auto <= t <= t_move]
        t_cmd = next((t for t, v, _ in run_cmd if v >= STOP_SPEED), None)
        print(f"  출발 지연 구간 명령: 최대 속도 {max((v for _, v, _ in run_cmd), default=0):.2f} m/s, "
              f"최대 가속도 {max((a for _, _, a in run_cmd), default=0):.2f} m/s², "
              f"명령 속도 첫 ≥{STOP_SPEED}: " + (f"AUTO+{t_cmd - t_auto:.1f} s" if t_cmd else "없음"))
    else:
        print("출발 지연: AUTO 후 한 번도 움직이지 않음")
    print(f"속도 최대 {max(v for _, v in run_speed) * 3.6:.1f} km/h, "
          f"평균 {sum(v for _, v in run_speed) / len(run_speed) * 3.6:.1f} km/h")
    print(f"NVTL 최소 {min(vals):.2f} / 평균 {sum(vals) / len(vals):.2f} / 최대 {max(vals):.2f}, "
          f"{NVTL_MIN_OK} 미만 {sum(v < NVTL_MIN_OK for v in vals)}/{len(vals)}건")
    print(f"중간 정지(≥{STOP_MIN_SEC}s): {len(stops)}회",
          [f"AUTO+{s:.1f}s 동안 {d:.1f}s" + (" (끝까지 정지)" if end else "") for s, d, end in stops])
    print("velocity_factors (behavior, status): 건수")
    for (b, s), n in behaviors.most_common():
        print(f"  {b!r}, {s}: {n}")
    print("planning_factors (module, behavior, detail): 건수")
    for (m, b, d), n in pfactors.most_common():
        print(f"  {m}, {b}, {d!r}: {n}")
    if goal and last_pos:
        print(f"최종 위치 ({last_pos.x:.2f}, {last_pos.y:.2f}), "
              f"goal 오차 {math.hypot(last_pos.x - goal[0], last_pos.y - goal[1]):.2f} m")


if __name__ == "__main__":
    main()