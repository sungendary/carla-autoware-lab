# Environment

> 이 파일은 "내 환경에서 어떻게 실행하는지"를 담는다.
> 설치하거나 문제를 해결할 때마다 바로 추가한다. 나중의 내가 이것만 보고 재현할 수 있으면 성공.

## 하드웨어

| 항목 | 사양 |
|---|---|
| GPU | NVIDIA GeForce RTX 5070 Ti (16GB) |
| CPU | AMD Ryzen 9 5900X (12코어) |
| RAM | DDR4 64GB |
| 저장장치 | SSD 2TB (Ubuntu 1.5TB / Windows 11 나머지, 듀얼부팅) |

## 소프트웨어 구성

| 항목 | 버전 | 상태 | 비고 |
|---|---|---|---|
| Host OS | Ubuntu 24.04.5 LTS (noble) | 설치됨 | |
| Kernel | 7.0.0-42-generic | 설치됨 | HWE 커널 |
| Secure Boot | enabled | - | 드라이버 모듈 서명 정상 |
| NVIDIA Driver | 595.99.02 (open kernel module) | 설치됨 | 패키지 `nvidia-driver-595-open`(apt), 지원 CUDA 최대 13.2. RTX 50은 570+ 및 -open 필수 |
| Docker Engine | 29.9.0 (docker-ce, 공식 apt 저장소) | 설치됨 | rootful 모드, 사용자 docker 그룹 포함. compose 5.6.0 / buildx 0.38.0 / containerd 2.4.1 |
| NVIDIA Container Toolkit | 1.20.1-1 (nvidia.github.io stable 저장소) | 설치됨 | `/etc/docker/daemon.json`에 nvidia 런타임 등록 |
| Autoware | universe-cuda-humble-2.0.0 | 설치됨 | ghcr.io/autowarefoundation/autoware, digest sha256:42df03619cb9c417e232ca8a7f8e483187f9fe07d1ff07247f0d44aecab67bff, 디스크 22.8GB / 압축 7.06GB, CUDA 12.8 (/usr/local/cuda-12.8), 컨테이너 사용자 aw(UID 1000) |
| Autoware 참고 저장소 | autowarefoundation/autoware @2.0.0 | 클론됨 | ~/autoware, 빌드 안 함. 문서·ansible 참고용 |
| DDS 수신 버퍼 | net.core.rmem_max=2147483647 | 적용됨 | /etc/sysctl.d/10-cyclone-max.conf (커널 기본 4194304) |
| CARLA | 0.9.16 | 설치됨 | Docker carlasim/carla:0.9.16, digest sha256:aaf1df22702780ece072069e23d03c4879b002ae028c79744b09c4c7ddbae953, 29.4GB, 컨테이너 workdir /workspace, 사용자 carla |
| CARLA Python 클라이언트 | carla 0.9.16 (cp310 wheel, manylinux_2_31) | 설치됨 | conda env carla, conda-forge, Python 3.10.22 (Autoware Humble 컨테이너와 같은 3.10) |

## 경로

| 용도 | 경로 |
|---|---|
| 저장소 | `~/Desktop/develop/carla-autoware-lab` |
| CARLA 서버 이미지 | carlasim/carla:0.9.16 (호스트 설치 없음) |
| CARLA Python 클라이언트 | `~/miniconda3/envs/carla` |
| Autoware 맵·데이터 | `~/autoware_data` (컨테이너 `/autoware_data`) |
| 샘플 맵 | `~/autoware_data/maps/sample-map-planning` (zip sha256:5536fce7bb8db7688fdf94ec004118b898637ad0d5b6175108b10989dd6e93b9, 2.0.0 demo_artifacts role 기준) |

대용량 파일(CARLA 본체, 맵, rosbag)은 저장소에 넣지 않고 위 경로에 둔다.

## 자주 쓰는 명령

```bash
# GPU 확인
nvidia-smi
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv

# 로드된 드라이버 모듈 확인 (Open Kernel Module 여부)
cat /proc/driver/nvidia/version

# 컨테이너 내 GPU 확인 (Toolkit이 호스트 드라이버를 주입하는지)
docker run --rm --gpus all ubuntu nvidia-smi

# (설치하면서 추가)
```

### Autoware planning simulator

```bash
# [사전·최초 1회] DDS 수신 버퍼 상한 영구 적용 (재부팅 후에도 유지)
echo 'net.core.rmem_max=2147483647' | sudo tee /etc/sysctl.d/10-cyclone-max.conf
sudo sysctl --system | grep rmem_max
# [매 실행 전 확인]
sysctl net.core.rmem_max   # 2147483647이어야 함

# [최초 1회] 샘플 맵 (URL·해시는 autoware 2.0.0 ansible/roles/demo_artifacts 기준)
mkdir -p ~/autoware_data/maps && cd ~/autoware_data/maps
wget -O sample-map-planning.zip https://autoware-files.s3.us-west-2.amazonaws.com/maps/demos/sample-map-planning.zip
echo "5536fce7bb8db7688fdf94ec004118b898637ad0d5b6175108b10989dd6e93b9  sample-map-planning.zip" | sha256sum -c -
unzip -o sample-map-planning.zip -d ~/autoware_data/maps

# Autoware 컨테이너 실행
IMG=ghcr.io/autowarefoundation/autoware:universe-cuda-humble-2.0.0
xhost +local:docker
docker run -it --rm --name autoware \
  --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v /etc/localtime:/etc/localtime:ro \
  --cap-add=NET_ADMIN --ipc host \
  -v $HOME/autoware_data:/autoware_data \
  $IMG

# (컨테이너 안) planning simulator
ros2 launch autoware_launch planning_simulator.launch.xml \
  map_path:=/autoware_data/maps/sample-map-planning \
  vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit

# 두 번째 셸 (exec는 entrypoint를 거치지 않아 기본 root로 열림 → -u aw + source)
docker exec -it -u aw autoware bash
source /opt/ros/humble/setup.bash && source /opt/autoware/setup.bash

# 상태 확인 (RViz: P → G → AUTO)
timeout 5 ros2 topic echo /api/localization/initialization_state --once  # 3
timeout 5 ros2 topic echo /api/routing/state --once                      # 2 SET / 3 ARRIVED
timeout 5 ros2 topic echo /api/operation_mode/state --once               # mode 2 = AUTONOMOUS

# 종료 후 X 접근 권한 원복
xhost -local:docker
```

### CARLA 단독 실행

```bash
# [최초 1회] 서버 이미지
docker pull carlasim/carla:0.9.16
# [최초 1회] Python 클라이언트 (conda-forge만 사용: 기본 채널 약관 프롬프트 회피)
conda create -n carla -c conda-forge --override-channels python=3.10 -y
conda activate carla && python -m pip install carla==0.9.16

# 서버 실행 (GUI). 포트는 로컬에만 노출 (CARLA는 인증 없음, Docker 포트는 ufw 우회)
xhost +local:docker
docker run -d --rm --name carla \
  --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -p 127.0.0.1:2000-2002:2000-2002 \
  carlasim/carla:0.9.16 bash CarlaUE4.sh -nosound
# 화면 없이: 위에서 DISPLAY·X11 줄을 빼고 -RenderOffScreen 추가
# 로그는 "Disabling core dumps."에서 멈춘 것처럼 보이는 것이 정상 → 접속으로 확인
python -c "import carla; c=carla.Client('localhost',2000); c.set_timeout(10); print(c.get_client_version(), c.get_server_version())"  # 0.9.16 0.9.16

# Town01 + 오토파일럿 (동기 모드, 시드 고정)
python scripts/carla/spawn_autopilot.py --duration 60 --seed 42

# 종료
docker stop carla && xhost -local:docker
```

포트 바인딩(127.0.0.1)은 Phase 1에서 브리지 연결 방식에 따라 재검토 (D-007과 함께)

## 트러블슈팅 기록

형식: 날짜 / 증상 / 원인 / 해결

<!-- 예시
### 2026-11-06 / nvidia-smi에서 GPU가 안 보임
- 원인:
- 해결:
-->

### 2026-11-07 / 컨테이너 시작 시 entrypoint 경고 "ip link set lo multicast on" 실패
- 원인: 이미지의 CycloneDDS 설정이 lo 전용 + multicast 사용인데, 컨테이너에 NET_ADMIN 권한이 없음. --net host에서 이 권한을 주면 호스트 lo가 바뀜
- 해결: --net host 없이 Docker 기본 bridge 네트워크(--net 지정 없음) + --cap-add=NET_ADMIN → 경고 사라짐, lo MULTICAST 확인. Phase 1(다른 컨테이너와 통신)에서 재검토

### 2026-11-07 / launch 즉시 "failed to increase socket receive buffer size to at least 10485760 bytes, current is 8388608" + rmw_create_node 실패
- 원인: 호스트 net.core.rmem_max = 4194304(커널 기본값) < cyclonedds.xml의 SocketReceiveBufferSize min 10MB. 컨테이너는 호스트 상한을 따름(8MB = 4MB × 2)
- 해결: sudo sysctl -w net.core.rmem_max=2147483647로 확인 후, /etc/sysctl.d/10-cyclone-max.conf로 영구 적용

### 2026-11-07 / AUTO 후 kinematic_state 속도 0
- 원인: 오류 아님. 초기 위치(P) 전에는 kinematic_state가 발행되지 않고, AUTO 직후에는 가속 전
- 확인: 반복 측정 시 약 2.78 m/s(10 km/h) 정속 주행, 도착 시 routing/state 3

### 2026-11-07 / venv 생성 실패 "ensurepip is not available"
- 원인: Ubuntu 24.04 시스템 Python에 python3.12-venv 미설치
- 해결: 시스템 패키지 설치 대신 miniconda env(Python 3.10)로 전환 (D-002)

## 검증 범위

- GPU: 컨테이너 내 OpenGL 렌더링 확인 (nvidia-smi에서 rviz2 Type G). CUDA 연산은 planning simulator에서 사용하지 않아 미검증
- rmem_max 영구 적용: 재부팅 후 유지 확인 (2026-11-07, 부팅 16:46:47 이후 2147483647)
- CARLA VRAM (GUI·기본 품질): 기준 481 MiB → Town10HD 6989 MiB(약 6.5GB 사용), Town01 4846 MiB(약 4.3GB 사용) / 총 16303 MiB
- CARLA 재현성: 동기 모드(0.05 s) + TM 시드 42로 2회 실행 시 스폰 좌표·속도·이동거리 동일 (액터 id는 실행마다 다름)
- 실제 확인한 서버 실행은 0.0.0.0 바인딩(-p 2000-2002:2000-2002). 127.0.0.1 바인딩 명령은 다음 실행 때 확인
