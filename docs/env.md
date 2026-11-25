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
| NVIDIA Driver | 595.99.02 (open kernel module) | 설치됨 | 패키지 `nvidia-driver-595-open`(apt, Ubuntu 공식 noble-updates/restricted), 커널 모듈은 `nvidia-dkms-595-open`(DKMS 빌드, MOK 서명). 지원 CUDA 최대 13.2. RTX 50은 570+ 및 -open 필수 |
| Docker Engine | 29.9.0 (docker-ce, 공식 apt 저장소) | 설치됨 | rootful 모드, 사용자 docker 그룹 포함. compose 5.6.0 / buildx 0.38.0 / containerd 2.4.1 |
| NVIDIA Container Toolkit | 1.20.1-1 (nvidia.github.io stable 저장소) | 설치됨 | `/etc/docker/daemon.json`에 nvidia 런타임 등록 |
| Autoware | universe-cuda-humble-2.0.0 | 설치됨 | ghcr.io/autowarefoundation/autoware, digest sha256:42df03619cb9c417e232ca8a7f8e483187f9fe07d1ff07247f0d44aecab67bff, 디스크 22.8GB / 압축 7.06GB, CUDA 12.8 (/usr/local/cuda-12.8), nvcc 12.8(/usr/local/cuda-12.8/bin/nvcc), TensorRT libnvinfer10 10.8.0.43-1+cuda12.8, 컨테이너 사용자 aw(UID 1000) |
| Autoware 참고 저장소 | autowarefoundation/autoware @2.0.0 | 클론됨 | ~/autoware, 빌드 안 함. 문서·ansible 참고용 |
| DDS 수신 버퍼 | net.core.rmem_max=2147483647 | 적용됨 | /etc/sysctl.d/10-cyclone-max.conf (커널 기본 4194304) |
| CARLA | 0.9.16 | 설치됨 | Docker carlasim/carla:0.9.16, digest sha256:aaf1df22702780ece072069e23d03c4879b002ae028c79744b09c4c7ddbae953, 29.4GB, 컨테이너 workdir /workspace, 사용자 carla |
| Miniconda | conda 26.7.1 | 설치됨 | ~/miniconda3, conda init bash |
| CARLA Python 클라이언트 | carla 0.9.16 (cp310 wheel, manylinux_2_31) | 설치됨 | conda env carla, conda-forge, Python 3.10.22 (Autoware Humble 컨테이너와 같은 3.10) |
| GitHub CLI | gh 2.103.3 | 설치됨 | cli.github.com/packages(공식 apt), gh auth login(HTTPS), 토큰은 시스템 keyring 저장, git 인증 도우미는 github.com 전용 |
| git-lfs | 3.8.1 | 설치됨 | packagecloud.io/github/git-lfs(apt), 2026-11-15 설치. LFS 필터 설정(filter.lfs.*)은 ~/.gitconfig. Town01 자산(LFS 파일) 받기용 |
| autoware_carla_interface | autoware_universe 0.53.1 (2.0.0 이미지 포함) | 확인됨 | /opt/autoware/autoware_carla_interface, launch: autoware_carla_interface.launch.xml, e2e_simulator simulator_type:=carla |
| 컨테이너용 CARLA Python | carla 0.9.16 휠 | 준비됨 | ~/autoware_deps/carla-0.9.16-site (휠 동일 폴더 ~/autoware_deps에 보관), 휠 sha256 52b1f2fafb0655e25954f9f6d1e97c211a4da404217fd1d0094b4b7350737c95 (D-010) |
| Hugging Face CLI | huggingface_hub 1.29.0 (hf) | 설치됨 | conda env hf (conda-forge, Python 3.10.22), 인지 모델 다운로드용 |
| LiDAR 검출 모델 | lidar_centerpoint v4.1 | 받음 | HF AutowareFoundation/lidar_centerpoint, 커밋 462469f02ff658cc9e803eb058fb79b086c480cd, 19 files 71M, 파일별 sha256: ~/autoware_data/ml_models/lidar_centerpoint_v4.1.sha256. 출처 근거: autoware 2.0.0 ansible/roles/artifacts (role에 체크섬 없음) |
| Open AD Kit 참고 저장소 | openadkit @c7586a131cae7dae8c8fa2daf96c3bc7814ca6dd (2026-11-09) | 클론됨 | ~/openadkit, 실행 안 함. CARLA 연동 비교 기준 |

## 경로

| 용도 | 경로 |
|---|---|
| 저장소 | `~/Desktop/develop/carla-autoware-lab` |
| CARLA 서버 이미지 | carlasim/carla:0.9.16 (호스트 설치 없음) |
| CARLA Python 클라이언트 | `~/miniconda3/envs/carla` |
| Autoware 맵·데이터 | `~/autoware_data` (컨테이너 `/autoware_data`) |
| 컨테이너용 CARLA Python | `~/autoware_deps/carla-0.9.16-site` (컨테이너 `/opt/carla-py`, 읽기 전용, D-010) |
| 샘플 맵 | `~/autoware_data/maps/sample-map-planning` (zip sha256:5536fce7bb8db7688fdf94ec004118b898637ad0d5b6175108b10989dd6e93b9, 2.0.0 demo_artifacts role 기준) |
| 인지 모델 | `~/autoware_data/ml_models` (현재 `-v $HOME/autoware_data:/autoware_data` 마운트로 쓰기 가능(TensorRT 엔진 생성에 필요). e2e_simulator data_path 기본값은 `$HOME/autoware_data/ml_models` → 컨테이너 `/autoware_data` 마운트와 불일치, e2e 실행 명령에서 `data_path:=/autoware_data/ml_models` 지정) |
| Town01 맵 | `~/autoware_data/maps/Town01` (lanelet2_map.osm, pointcloud_map.pcd, map_projector_info.yaml: projector_type: Local). 2026-11-15 해시 확인, 원본 `~/autoware_src/autoware-contents`. lanelet2_map.osm은 lanelet이 subtype road 124개뿐이고 traffic_light 규제 요소·turn_direction이 없음 → 신호 인식 설정(use_traffic_light_recognition)은 주행에 영향 없음, CARLA 신호등 무시·교차로 양보 미동작(교통 시나리오 한계, #15) |
| autoware_carla_interface 설치 위치 | `/opt/autoware/autoware_carla_interface/local/lib/python3.10/dist-packages/autoware_carla_interface` (컨테이너 안) |
| RViz 설정 (CARLA 확인용) | `~/autoware_data/rviz/carla_check.rviz` (컨테이너 `/autoware_data/rviz/carla_check.rviz`) |
| 실행 로그 | `~/autoware_data/logs` (컨테이너 `/autoware_data/logs`) |
| rosbag | `~/autoware_data/rosbags` (컨테이너 `/autoware_data/rosbags`), 파일명 `{이슈}_{내용}_{MMDD_HHMM}` (예: 15_driveB_cli_1125_1839) |
| 캡처 | `docs/images/{이슈번호}_{내용}[_{기준}].{png\|pdf}` (예: 14_rviz_sensing_base_link.png, 14_tf_frames.pdf) |

Town01 자산 출처 (openadkit deployment.json 기준)
- Town01.osm: https://bitbucket.org/carla-simulator/autoware-contents/raw/062f94b5322e679ee0430e2daa6995dca9f7f0ea/maps/vector_maps/lanelet2/Town01.osm sha256 5e3c0873004666a399494a59048b93ecfbd1d40433c29d29e7319847a2a8afa2
- Town01.pcd: https://bitbucket.org/carla-simulator/autoware-contents/raw/062f94b5322e679ee0430e2daa6995dca9f7f0ea/maps/point_cloud_maps/Town01.pcd sha256 296d6429ae0190b19a35458a155d76d8e3c4f460eb718cde3d669bc5a8f03ba2
- 위 raw URL 2개: 불가(2026-11-15, GET 404·HEAD 403, openadkit deployment.json과 동일). 두 파일은 Git LFS로 저장되어 있어 아래처럼 받는다
- 확인 결과: LFS 포인터 oid = 위 sha256과 일치, 크기 472955 B(osm)·190275004 B(pcd). PCD는 v0.7, FIELDS x y z, 16726884 pts, DATA binary_compressed. osm은 node 1848개 모두 local_x 태그 보유(map_projector_info Local과 맞음)

```bash
# [최초 1회] Town01 자산: 필요한 두 파일만 sparse checkout + LFS pull (git-lfs 필요)
mkdir -p ~/autoware_src && cd ~/autoware_src
git clone --filter=blob:none --no-checkout https://bitbucket.org/carla-simulator/autoware-contents.git
cd autoware-contents
git sparse-checkout set --no-cone /maps/vector_maps/lanelet2/Town01.osm /maps/point_cloud_maps/Town01.pcd
# checkout 중 LFS 다운로드는 진행률이 없어 멈춘 것처럼 보임 → 포인터만 받고 lfs pull로 분리
GIT_LFS_SKIP_SMUDGE=1 git checkout -f 062f94b5322e679ee0430e2daa6995dca9f7f0ea
git lfs pull --include="maps/vector_maps/lanelet2/Town01.osm,maps/point_cloud_maps/Town01.pcd"

mkdir -p ~/autoware_data/maps/Town01
cp maps/vector_maps/lanelet2/Town01.osm ~/autoware_data/maps/Town01/lanelet2_map.osm
cp maps/point_cloud_maps/Town01.pcd ~/autoware_data/maps/Town01/pointcloud_map.pcd
echo 'projector_type: Local' > ~/autoware_data/maps/Town01/map_projector_info.yaml
chmod 644 ~/autoware_data/maps/Town01/*
cd ~/autoware_data/maps/Town01
sha256sum -c - <<'EOF'
5e3c0873004666a399494a59048b93ecfbd1d40433c29d29e7319847a2a8afa2  lanelet2_map.osm
296d6429ae0190b19a35458a155d76d8e3c4f460eb718cde3d669bc5a8f03ba2  pointcloud_map.pcd
EOF
```

대용량 파일(CARLA 본체, 맵, rosbag)은 저장소에 넣지 않고 위 경로에 둔다.

## 자주 쓰는 명령

### 설치 (최초 1회, 순서대로)

```bash
# 1) NVIDIA 드라이버: Ubuntu 공식 저장소(noble-updates/restricted), DKMS 빌드 + MOK 서명
sudo apt update
sudo apt install nvidia-driver-595-open
# Secure Boot: 설치 중 MOK 비밀번호 설정 → 재부팅 시 "Enroll MOK" → Continue → 비밀번호 입력
#   (MOK 키가 이미 등록된 PC면 이 화면이 나오지 않음)
sudo reboot
cat /proc/driver/nvidia/version                       # Open Kernel Module 595.99.02
dkms status                                           # 설치된 커널마다 nvidia/595.99.02 ... installed
modinfo -F signer nvidia                              # <호스트명> Secure Boot Module Signature key
mokutil --test-key /var/lib/shim-signed/mok/MOK.der   # already enrolled (앞의 keyring 경고는 무시)
# 커널 업데이트 후 dkms status로 새 커널 빌드 확인. 이전 커널 빌드가 남아 있으면 GRUB에서 그 커널로 복구 가능

# 2) Docker Engine: 공식 apt 저장소 (deb822 형식)
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<'EOF'
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
sudo usermod -aG docker $USER        # 로그아웃 후 적용, groups로 docker 포함 확인
# 버전은 고정하지 않음(보안 업데이트). 업그레이드 후 아래 GPU 컨테이너 확인을 다시 실행

# 3) NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker   # daemon.json에 nvidia 런타임 등록(기본 런타임 아님 → --gpus all 필요)
sudo systemctl restart docker
docker run --rm --gpus all ubuntu nvidia-smi

# 4) Miniconda (CARLA Python 클라이언트용, 검증 시 conda 26.7.1)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
~/miniconda3/bin/conda init bash      # 새 셸부터 (base) 자동 활성화

# 5) GitHub CLI: 공식 apt 저장소 (Ubuntu 기본 저장소 버전은 오래됨) (D-008)
sudo mkdir -p -m 755 /etc/apt/keyrings
wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh
gh auth login      # GitHub.com → HTTPS → Authenticate Git: Yes → Login with a web browser
gh auth status     # Logged in ... (keyring), Token scopes에 repo 포함

# 6) git-lfs: packagecloud.io/github/git-lfs (Town01 자산 받기용)
#    이 PC는 저장소가 이미 등록되어 있었음(/etc/apt/sources.list.d/github_git-lfs.list, packagecloud 스크립트가 생성)
#    새 PC(공식 안내, 이 PC에서는 미실행): curl -fsSL https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install git-lfs
git lfs version    # git-lfs/3.8.1
git config --global --get-regexp '^filter\.lfs'   # 필터 설정이 없으면 git lfs install
```

호스트에 등록된 기타 저장소
- 이 프로젝트에서 사용: packagecloud.io/github/git-lfs (git-lfs)
- 이 프로젝트와 무관: graphics-drivers PPA(595는 이 PPA가 아닌 공식 저장소에서 설치), ubuntu-toolchain-r test PPA(호스트 gcc 갱신, 컨테이너에는 영향 없음)

```bash
# GPU 확인
nvidia-smi
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv

# 로드된 드라이버 모듈 확인 (Open Kernel Module 여부)
cat /proc/driver/nvidia/version

# 컨테이너 내 GPU 확인 (Toolkit이 호스트 드라이버를 주입하는지)
docker run --rm --gpus all ubuntu nvidia-smi
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
curl -fL -o sample-map-planning.zip https://autoware-files.s3.us-west-2.amazonaws.com/maps/demos/sample-map-planning.zip
echo "5536fce7bb8db7688fdf94ec004118b898637ad0d5b6175108b10989dd6e93b9  sample-map-planning.zip" | sha256sum -c -
unzip -o sample-map-planning.zip -d ~/autoware_data/maps

# [최초 1회] 이미지 (기록된 digest로 pull → 실행에 쓰는 태그 부여)
docker pull ghcr.io/autowarefoundation/autoware@sha256:42df03619cb9c417e232ca8a7f8e483187f9fe07d1ff07247f0d44aecab67bff
docker tag ghcr.io/autowarefoundation/autoware@sha256:42df03619cb9c417e232ca8a7f8e483187f9fe07d1ff07247f0d44aecab67bff \
  ghcr.io/autowarefoundation/autoware:universe-cuda-humble-2.0.0

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
# [최초 1회] 서버 이미지 (기록된 digest로 pull → 실행에 쓰는 태그 부여)
docker pull carlasim/carla@sha256:aaf1df22702780ece072069e23d03c4879b002ae028c79744b09c4c7ddbae953
docker tag carlasim/carla@sha256:aaf1df22702780ece072069e23d03c4879b002ae028c79744b09c4c7ddbae953 carlasim/carla:0.9.16
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
conda activate carla   # 새 터미널마다 필요
python -c "import carla; c=carla.Client('localhost',2000); c.set_timeout(10); print(c.get_client_version(), c.get_server_version())"  # 0.9.16 0.9.16

# Town01 + 오토파일럿 (동기 모드, 시드 고정)
cd ~/Desktop/develop/carla-autoware-lab   # 저장소 루트 (스크립트가 상대 경로)
python scripts/carla/spawn_autopilot.py --duration 60 --seed 42

# 종료
docker stop carla && xhost -local:docker
```

### CARLA ↔ Autoware 연결 (#13, #14)

호스트 공개는 127.0.0.1:2000-2002 유지, 컨테이너 사이는 사용자 정의 bridge 네트워크 carla-aw (D-009). Town01 e2e 실행 명령은 이 절 끝(#14).

```bash
# [최초 1회] 사용자 정의 bridge 네트워크 (재부팅 후에도 유지, 지우지 않음)
docker network create carla-aw
docker network inspect carla-aw --format '{{.Driver}} {{range .IPAM.Config}}{{.Subnet}}{{end}}'  # bridge 172.18.0.0/16

# [최초 1회] 컨테이너용 CARLA Python 위치 (D-010): 휠·압축 해제 폴더 모두 ~/autoware_deps
#   휠 sha256 52b1f2fafb0655e25954f9f6d1e97c211a4da404217fd1d0094b4b7350737c95

# CARLA 서버 (Phase 0 명령 + --network carla-aw)
xhost +local:docker
docker run -d --rm --name carla --network carla-aw \
  --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -p 127.0.0.1:2000-2002:2000-2002 \
  carlasim/carla:0.9.16 bash CarlaUE4.sh -nosound

# Autoware (Phase 0 명령 + --network carla-aw + 휠 마운트 + PYTHONPATH)
IMG=ghcr.io/autowarefoundation/autoware:universe-cuda-humble-2.0.0
docker run -it --rm --name autoware --network carla-aw \
  --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v /etc/localtime:/etc/localtime:ro \
  --cap-add=NET_ADMIN --ipc host \
  -v $HOME/autoware_data:/autoware_data \
  -v $HOME/autoware_deps/carla-0.9.16-site:/opt/carla-py:ro \
  -e PYTHONPATH=/opt/carla-py \
  $IMG

# 연결 확인 (두 번째 셸: docker exec -it -u aw autoware bash)
getent hosts carla                                  # 172.18.0.x carla
for p in 2000 2001 2002; do timeout 3 bash -c "</dev/tcp/carla/$p" && echo "$p open" || echo "$p closed"; done

# 서버 버전 + 스트리밍 (호스트, 저장소 루트에서. stdin으로 넘겨 저장소 마운트 불필요)
#   e2e 실행 중에는 카메라 액터를 추가하므로 쓰지 않는다. 단독 확인에서 서버가 동기 모드로 남아 있으면 --tick
cd ~/Desktop/develop/carla-autoware-lab
docker exec -i -u aw autoware python3 - --host carla < scripts/carla/check_connection.py
conda activate carla && python scripts/carla/check_connection.py --host localhost

# 노출 범위
docker port carla; docker port autoware
sudo ss -tlnp | grep -E ':200[0-2]\b'
docker network inspect carla-aw --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
LAN_IP=$(ip -4 route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}')
timeout 3 bash -c "</dev/tcp/$LAN_IP/2000" && echo "LAN 노출됨(문제)" || echo "LAN 차단(정상)"

# CUDA 연산
docker exec -i -u aw autoware python3 - < scripts/check/cuda_vadd.py

# (컨테이너 안, ROS 소싱 후) centerpoint TensorRT 엔진만 빌드 후 종료
ros2 launch autoware_lidar_centerpoint lidar_centerpoint.launch.xml \
  data_path:=/autoware_data/ml_models build_only:=true
find /autoware_data/ml_models/lidar_centerpoint -name '*.engine'

# 종료 (네트워크는 유지)
exit                                        # (컨테이너 셸)
docker stop carla && xhost -local:docker    # (호스트)
```

Town01 e2e 실행 (#14). CARLA·Autoware 컨테이너는 위 명령으로 띄운 상태에서 시작한다. ego 스폰 위치는 D-012.

```bash
# (Autoware 컨테이너 안) e2e_simulator + CARLA, 로그는 /autoware_data/logs에 저장
ISSUE=15   # 로그 파일명 {이슈}_e2e_{MMDD_HHMM}.log → 진행 중인 이슈 번호로 바꿔 쓴다
ros2 launch autoware_launch e2e_simulator.launch.xml \
  map_path:=/autoware_data/maps/Town01 \
  vehicle_model:=sample_vehicle sensor_model:=carla_sensor_kit \
  simulator_type:=carla host:=carla port:=2000 \
  data_path:=/autoware_data/ml_models \
  use_light_weight_sensor_mapping:=true use_traffic_light_recognition:=false \
  spawn_point:="395.96, 249.43, 0.30, 0.0, 0.0, -90.0" spawn_point_ground_snap:=true \
  2>&1 | tee /autoware_data/logs/${ISSUE}_e2e_$(date +%m%d_%H%M).log
# spawn_point: CARLA 좌표·deg, 대괄호 없이 "x, y, z, roll, pitch, yaw". 6개가 아니면 오류 없이 랜덤 스폰

# 두 번째 셸 (호스트에서)
docker exec -it -u aw autoware bash
source /opt/ros/humble/setup.bash && source /opt/autoware/setup.bash

# 상태 확인
ros2 param get /autoware_carla_interface host                              # String value is: carla
timeout 5 ros2 topic echo /api/localization/initialization_state --once  # state 3 (GNSS 자동 초기화)
timeout 10 ros2 topic hz /clock                                            # 약 20 Hz (RTF≈1)
timeout 10 ros2 topic hz /sensing/lidar/concatenated/pointcloud            # 약 10 Hz
```

- RViz 설정: `/autoware_data/rviz/carla_check.rviz` (File → Open Config). 기본 autoware.rviz는 덮어쓰지 않는다. 값 편집은 Displays 패널의 값 칸을 더블클릭
- 종료 후 CARLA 동기 모드: Autoware만 Ctrl-C로 종료하면 동기 모드 True(fixed_delta 0.05)가 남는다. ego·센서 액터는 정리되고, 다시 launch하면 같은 위치에 재스폰된다(#15). 동기 모드가 남아 있으므로 Autoware가 꺼진 동안 tick을 보내지 않는 클라이언트는 응답을 기다리며 멈춘다(check_connection.py는 --tick). CARLA 컨테이너를 새로 띄우면 기본 비동기

### Town01 고정 경로 주행 (#15)

출발지·목적지는 고정한다(D-012, D-013). CARLA·Autoware 컨테이너는 위 "CARLA ↔ Autoware 연결" 명령으로 띄운 상태에서 시작한다.

- 고정 출발지: D-012 그대로 (map (395.99, −250.85) yaw 90°). 재스폰 2회 위치 차이 1 cm 이내
- 고정 목적지(goal B): map (252.83, 2.25, 0.0), yaw 180° = 쿼터니언 (0, 0, 1, 0). 직선 약 250 m 후 교차로 좌회전, 약 143 m, 총 약 390 m
- 절차: e2e launch → initialization_state 3·kinematic_state 출발지 확인 → 녹화 시작 → set_route_points → routing/state 2·is_autonomous_mode_available True → change_to_autonomous → routing/state 3 확인 후 몇 초 뒤 녹화 종료 → bag_summary.py
- 도착하면 operation_mode가 자동으로 1(STOP)이 된다 → 회차마다 AUTO 필요
- 회차 사이: launch를 Ctrl-C로 끄고 다시 launch (CARLA 재시작 불필요)

```bash
ISSUE=16   # 이슈 번호. 셸마다 정의한다(launch 셸에서 정한 값은 다른 셸에 없음)

# (Autoware 컨테이너 안, 두 번째 셸) 1) 위 e2e launch 후 상태 확인
timeout 5 ros2 topic echo /api/localization/initialization_state --once  # state 3
timeout 5 ros2 topic echo /localization/kinematic_state --once --field pose.pose  # (395.99, −250.85) 부근

# 2) 녹화 (세 번째 셸에서도 ISSUE= 먼저 정의, 파일명 {이슈}_{내용}_{MMDD_HHMM})
ros2 bag record -o /autoware_data/rosbags/${ISSUE:?ISSUE를 먼저 정의}_driveB_cli_$(date +%m%d_%H%M) -e '^(/localization/kinematic_state|/localization/pose_estimator/nearest_voxel_transformation_likelihood|/api/routing/state|/api/operation_mode/state|/api/planning/velocity_factors|/control/command/control_cmd|/planning/planning_factors/.*)$'

# 3) 목적지 지정 → routing/state 2, is_autonomous_mode_available True 확인
ros2 service call /api/routing/set_route_points autoware_adapi_v1_msgs/srv/SetRoutePoints "{header: {frame_id: map}, option: {allow_goal_modification: false}, goal: {position: {x: 252.83, y: 2.25, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 1.0, w: 0.0}}, waypoints: []}"
timeout 5 ros2 topic echo /api/routing/state --once                 # state 2 SET
timeout 5 ros2 topic echo /api/operation_mode/state --once          # is_autonomous_mode_available: true
# 지정된 goal 확인 (route는 TRANSIENT_LOCAL이라 QoS 지정 필요)
timeout 5 ros2 topic echo /planning/mission_planning/route --once --field goal_pose \
  --qos-durability transient_local --qos-reliability reliable

# 4) AUTO → routing/state 3(ARRIVED) 확인 후 몇 초 뒤 녹화 셸에서 Ctrl-C
ros2 service call /api/operation_mode/change_to_autonomous autoware_adapi_v1_msgs/srv/ChangeOperationMode {}

# 5) (호스트, 저장소 루트) 주행 요약: AUTO→ARRIVED 시간·출발 지연·속도·NVTL·중간 정지·goal 오차
cd ~/Desktop/develop/carla-autoware-lab
docker exec -i -u aw autoware bash -c "source /opt/ros/humble/setup.bash && source /opt/autoware/setup.bash && python3 - /autoware_data/rosbags/<bag> 252.83 2.25" < scripts/analysis/bag_summary.py

# (호스트, Autoware 정지 중에만) CARLA 상태: 맵·동기 모드·차량·센서 수 (읽기만 함, tick 없음)
conda activate carla && python scripts/carla/check_world_state.py
```

## 트러블슈팅 기록

형식: 날짜 / 증상 / 원인 / 해결

<!-- 예시
### 2026-11-06 / nvidia-smi에서 GPU가 안 보임
- 원인:
- 해결:
-->

### 2026-11-07 / 컨테이너 시작 시 entrypoint 경고 "ip link set lo multicast on" 실패
- 원인: 이미지의 CycloneDDS 설정이 lo 전용 + multicast 사용인데, 컨테이너에 NET_ADMIN 권한이 없음. --net host에서 이 권한을 주면 호스트 lo가 바뀜
- 해결: --net host 없이 Docker 기본 bridge 네트워크(--net 지정 없음) + --cap-add=NET_ADMIN → 경고 사라짐, lo MULTICAST 확인. Phase 1(다른 컨테이너와 통신)에서 재검토 → D-009에서 DDS는 컨테이너 내부 lo 유지로 결정

### 2026-11-07 / launch 즉시 "failed to increase socket receive buffer size to at least 10485760 bytes, current is 8388608" + rmw_create_node 실패
- 원인: 호스트 net.core.rmem_max = 4194304(커널 기본값) < cyclonedds.xml의 SocketReceiveBufferSize min 10MB. 컨테이너는 호스트 상한을 따름(8MB = 4MB × 2)
- 해결: sudo sysctl -w net.core.rmem_max=2147483647로 확인 후, /etc/sysctl.d/10-cyclone-max.conf로 영구 적용

### 2026-11-07 / AUTO 후 kinematic_state 속도 0
- 원인: 오류 아님. 초기 위치(P) 전에는 kinematic_state가 발행되지 않고, AUTO 직후에는 가속 전
- 확인: 반복 측정 시 약 2.78 m/s(10 km/h) 정속 주행, 도착 시 routing/state 3

### 2026-11-07 / venv 생성 실패 "ensurepip is not available"
- 원인: Ubuntu 24.04 시스템 Python에 python3.12-venv 미설치
- 해결: 시스템 패키지 설치 대신 miniconda env(Python 3.10)로 전환 (D-002)

### 2026-11-08 / 콜드 런 중 spawn_autopilot.py 실행 시 "No such file or directory"
- 원인: 스크립트를 저장소 기준 상대 경로로 실행하는데, env.md에는 "저장소 루트에서 실행" 주석만 있고 cd 명령이 없었음. 새 터미널은 홈(~)에서 시작
- 해결: spawn 명령 앞에 `cd ~/Desktop/develop/carla-autoware-lab` 추가. 문서 검증은 새 터미널에서 문서만 보고 실행(콜드 런)해서 한다

### 2026-11-08 / grep 패턴에 `<!--`를 큰따옴표로 넣었더니 다른 문자열로 바뀌어 실행됨
- 원인: bash 히스토리 확장. 큰따옴표 안에서도 `!`는 이전 명령 불러오기로 해석되고, bash는 바뀐 명령을 한 줄 출력한 뒤 실행함
- 해결: `!`가 들어간 패턴은 작은따옴표로 감싼다 (예: `grep -rn '<!--' docs/`)

### 2026-11-15 / 기존 휠 폴더 ~/autoware_data/python이 /autoware_data 마운트로 쓰기 가능하게 노출됨
- 원인: 상위 폴더(~/autoware_data) 전체를 rw로 마운트해서, 하위의 /opt/carla-py:ro 마운트와 별개로 /autoware_data/python 경로가 쓰기 가능
- 해결: ~/autoware_deps로 이동(휠 포함), D-010 갱신

### 2026-11-15 / 컨테이너 안에서 check_connection.py 실행 시 "RuntimeError: resolve: Host not found (authoritative)"
- 원인: CARLA 컨테이너가 꺼져 있었음. --rm이라 정지 시 삭제되고 carla-aw 내장 DNS에서 이름 carla도 사라짐
- 해결: CARLA를 --network carla-aw로 다시 실행하고, 약 20초 뒤 `docker exec -i -u aw autoware getent hosts carla`로 확인

### 2026-11-15 / Town01.osm·Town01.pcd를 Bitbucket raw URL로 받으면 404
- 원인: 두 파일이 Git LFS 파일이라 raw로 받지 못한 것으로 추정(GET 404·HEAD 403, 직접 원인은 미확인). 호스트에는 git-lfs가 설치되어 있지 않고 ~/.gitconfig에 LFS 필터 설정만 남아 있었음
- 해결: git-lfs 설치(apt, packagecloud.io/github/git-lfs) 후 sparse checkout + git lfs pull (명령은 경로 절 "Town01 자산 출처")
- 주의: checkout 중 LFS 다운로드(smudge)는 진행률이 표시되지 않아 멈춘 것처럼 보임 → `GIT_LFS_SKIP_SMUDGE=1`로 포인터만 checkout한 뒤 `git lfs pull`로 받음. 이번에는 중단된 checkout이 이미 받아 두어 lfs pull 출력 없음

### 2026-11-15 / e2e launch 직후 "Failed transform to map", "not part of the same tree" 반복, aggregator "Mode path not found"
- 원인: 오류 아님. 위치 초기화 전에는 map→base_link TF가 없어 변환이 실패함. aggregator 메시지는 시작 시 1회성
- 확인: GNSS 자동 초기화(state 3) 후 TF 경고 증가가 멈춤

### 2026-11-15 / RViz에 Town01 차선·점군 맵이 표시되지 않음
- 원인: 발행은 정상(/map/vector_map_marker·/map/pointcloud_map TRANSIENT_LOCAL). Lanelet2VectorMap은 Status Ok인데 Namespaces가 비어 있음 → 1회만 발행되는 메시지를 표시 항목이 받지 못한 상태. 점군 맵은 기본값(크기 1px, Alpha 0.2)이 너무 작고 흐림
- 해결: 표시 항목 체크를 껐다 다시 켜서 재구독 → 차선 표시됨. PointCloudMap은 Size 2·Alpha 0.6으로 변경 후 carla_check.rviz에 저장

### 2026-11-25 / launch 종료 후 ps에 python3 프로세스 1개 잔류
- 원인: ros2 CLI daemon(_ros2_daemon). 노드가 아님
- 해결: 무시해도 됨(종료해도 다음 ros2 명령 때 자동 재시작)

### 2026-11-25 / timeout으로 ros2 topic hz 종료 시 "failed to initialize wait set ... context is not valid"
- 원인: timeout이 강제 종료할 때 나오는 메시지
- 해결: 무시

## 검증 범위

- GPU: 컨테이너 내 OpenGL 렌더링 확인 (nvidia-smi에서 rviz2 Type G). CUDA 연산·TensorRT는 아래 2026-11-15 항목(#13)에서 확인
- rmem_max 영구 적용: 재부팅 후 유지 확인 (2026-11-07, 부팅 16:46:47 이후 2147483647)
- CARLA VRAM (GUI·기본 품질): 기준 481 MiB → Town10HD 6989 MiB(약 6.5GB 사용), Town01 4846 MiB(약 4.3GB 사용) / 총 16303 MiB (센서 미부착 기준). Town01 e2e(경량 매핑·RViz) 실행 시 VRAM max 8056/16303 MiB(CARLA 4284, centerpoint 컨테이너 1558, CUDA 컨테이너 3×~230 — #15에서 재현 안 됨), 상세는 아래 #14·#15 항목
- CARLA 재현성: 동기 모드(0.05 s) + TM 시드 42로 2회 실행 시 스폰 좌표·속도·이동거리 동일 (액터 id는 실행마다 다름)
- 서버 실행 명령(-p 127.0.0.1 바인딩) 확인 (2026-11-07, docker port에 127.0.0.1만 표시)
- 콜드 런: 2026-11-08 새 터미널에서 env.md만으로 Autoware planning simulator(P→G→AUTO, 도착)와 CARLA 스폰 재현. spawn 앞 cd 누락 1건 발견 후 수정
- CARLA 기준값(시드 42, Town01, 60 s): 스폰 x=396.0, y=249.4 / 60 s 이동거리 333.7 m
- Docker 디스크(2026-11-08): 이미지 78.19GB 중 이 프로젝트용은 Autoware 22.8GB·CARLA 29.4GB. 나머지(challenge-prediction 등)는 무관, 루트 여유 1.1TB라 유지. system df의 RECLAIMABLE에는 정지 중인 Autoware·CARLA도 포함되므로 prune -a 금지
- 2026-11-15 2.0.0 기본 sensor_mapping.yaml은 LiDAR·카메라 6대·IMU·GNSS 활성(Open AD Kit은 카메라 주석 처리). 경량 매핑(sensor_mapping_light_weight.yaml)은 LiDAR·CAM_FRONT 1대·IMU·GNSS 활성. 차이: 카메라 6대(1600x900, FOV 70/후방 110) → CAM_FRONT 1대(1080x720, FOV 120), LiDAR·카메라 주기 11 Hz → 10 Hz. LiDAR 파라미터(64ch, 100 m)·IMU(50 Hz)·GNSS(2 Hz)는 같음. e2e_simulator 인자 `use_light_weight_sensor_mapping:=true`로 선택(기본 False), `sensor_mapping_file`로 직접 지정도 가능
- 2026-11-15 e2e_simulator.launch.xml --show-args: CARLA 서버 지정 인자는 `host`(기본 localhost)·`port`(기본 2000), 접속 `timeout` 기본 20. 최상위 `host:=carla`는 launch 구조상(인자 없이 include) 전달될 것으로 판단 → #14에서 `ros2 param get /autoware_carla_interface host` = carla로 확인 (D-009). #13은 Python 클라이언트로 같은 경로(carla:2000/2001)만 확인. 그 밖에 `data_path` 기본 `$HOME/autoware_data/ml_models`, `carla_map`(기본 빈 값: map_path에서 이름 유도), `sync_mode` True, `fixed_delta_seconds` 0.05
- 2026-11-15 CARLA ↔ Autoware 연결 (#13)
  - 연결: autoware → carla 이름 해석 172.18.0.2, 2000·2001·2002 open (2002는 CARLA secondary 포트, 이 구성에서 미사용). IP는 컨테이너 시작 순서에 따라 바뀐다(재실행 시 autoware 172.18.0.2, carla 172.18.0.3). 접속은 항상 이름 carla로 한다
  - 서버 접속·스트리밍: 컨테이너(--host carla)와 호스트(--host localhost) 모두 client/server 0.9.16, 카메라 프레임 12·13장 수신 OK. 기본 맵 Town10HD_Opt, synchronous_mode=False
  - check_connection 동기 분기(리뷰 반영 cb2ef3b 후): 동기 모드 + tick 없음 0 frames FAIL(tick 안내) exit 1, 동기 모드 + --tick 10 frames OK exit 0 (확인 후 서버 비동기로 복원). 비동기 컨테이너·호스트 OK exit 0, cuda_vadd exit 0
  - 노출 범위: docker port carla는 127.0.0.1:2000-2002만, docker port autoware는 없음, ss는 docker-proxy 127.0.0.1만 LISTEN, LAN IP(192.168.219.133):2000 거부(호스트 자신에서 LAN IP로 접속 시도한 결과이며, 다른 기기에서는 미확인). carla-aw 구성원은 carla 172.18.0.2와 autoware 172.18.0.3뿐
  - CUDA 연산: RTX 5070 Ti, CC 12.0, 드라이버 API 13020, vadd N=1048576 불일치 0
  - TensorRT: libnvinfer10 10.8.0.43(Blackwell 지원 최소 버전대). centerpoint base 엔진 빌드 성공: pts_voxel_encoder.engine 18306644 B(3.6 s), pts_backbone_neck_head.engine 12630740 B(67.0 s), TRT 최대 GPU 909 MiB. 엔진은 GPU 아키텍처·TRT 버전에 종속되므로 저장소에 넣지 않음. short_range/sigma/tiny 변형은 미빌드. e2e는 base 변형을 씀(#14에서 확인, 이 엔진 재사용)
  - 무시해도 되는 경고: TRT "Network IO is empty, skipping validation", centerpoint "user_stream was not set ... CudaBlackboardSubscriber"(패키지 코드의 성능 경고)
- 2026-11-15 Town01 e2e 실행 (#14)
  - --show-args: `spawn_point`(최상위 인자, 기본 None = 랜덤, CARLA 좌표·deg, 대괄호 없이 "x, y, z, roll, pitch, yaw". 값이 6개가 아니면 오류 없이 랜덤 스폰, 파싱 시 z+2), `spawn_point_ground_snap`(기본 False, 켜면 지면+0.5), `lidar_detection_model` centerpoint(변형 이름 미지정 → base, #13 엔진 재사용), `use_traffic_light_recognition` 기본 true(이번 실행은 false)
  - host 전달: `ros2 param get /autoware_carla_interface host` = carla (#13의 "launch 구조상 전달될 것" 판단 확인, D-009)
  - 시계·주기: /clock 발행자는 autoware_carla_interface(자신은 use_sim_time False), Autoware 노드는 use_sim_time True, 메시지 stamp는 sim time. /clock 19.97 Hz(fixed_delta 0.05 s → RTF≈1). LiDAR /sensing/lidar/top/pointcloud_before_sync 9.99 Hz → /sensing/lidar/concatenated/pointcloud 9.98 Hz, CAM_FRONT 9.99 Hz
  - 맵 로드: lanelet2 로드 성공("no format_version" 경고는 무시), /map/vector_map·/map/vector_map_marker·/map/pointcloud_map 모두 TRANSIENT_LOCAL
  - 위치 추정: GNSS 자동 초기화 state 3(sim 13.9 s). kinematic_state (395.99, −250.85) yaw 90.1°, NDT NVTL 2.70 ≥ 2.3(converged_param_type 1). no_ground NVTL은 기본 미발행
  - 좌표 변환: CARLA (x, y, yaw) → map (x, −y, −yaw), 원점 같음(0). base_link는 CARLA 액터 중심에서 진행 반대 방향으로 wheelbase/2(1.425 m) 떨어진 점(후륜축 중심)
  - TF: map→base_link(EKF 20.2 Hz)·map→ndt_base_link(10.2 Hz)·map→viewer, base_link→sensor_kit_base_link→velodyne_top_base_link→velodyne_top, CAM×6(camera_link→camera_optical_link, 정적 TF는 sensor_kit 정의라 경량 매핑에서도 6대 모두 존재), tamagawa/imu_link, gnss_link. frame_id: before_sync = velodyne_top, concatenated = base_link, CAM_FRONT = CAM_FRONT/camera_optical_link
  - 자원(정지 상태, CARLA GUI·경량 매핑·RViz): VRAM max 8056/16303 MiB(CARLA 4284, centerpoint 컨테이너 1558, CUDA 컨테이너 3개 각 ~230), GPU util 평균 38.5%, CPU carla 223%·autoware 340%, load 5.07, 메모리 carla 2.55 GiB·autoware 27.65 GiB(5분간 변화 없음. component_container 4개 각 3.8~4.6 GB, rviz2 1.9 GB, pose_initializer 1.5 GB). 메모리 측정 방법 미기재(저장소·이슈 #14·PR #23에 기록 없음) → #15 docker stats 값(autoware 약 10 GiB)과 직접 비교 불가
  - VRAM 내역 중 그 밖 약 1.5 GiB와 CUDA 컨테이너 3개(각 ~230 MiB): #14 당시 미식별 → #15 재측정에서 CUDA 컨테이너 3개는 재현 안 됨, 그래픽 1089 MiB(Xorg 464, gnome-shell 92, rviz2 301, 기타 앱 2개 232) + 미할당 약 195 MiB로 확인(아래 #15 항목)
  - 캡처: [RViz sensing(base_link)](images/14_rviz_sensing_base_link.png), [CARLA ego top-down](images/14_carla_ego_topdown.png), [RViz localization(map)](images/14_rviz_localization_map.png), [TF 트리](images/14_tf_frames.pdf)
  - Autoware 종료 후 CARLA 동기 모드 잔존 여부: #15에서 확인(동기 모드 True 잔류, "CARLA ↔ Autoware 연결" 절)
- 2026-11-25 Town01 목적지 주행 (#15)
  - 출발지 D-012, goal은 D-013. 명령은 "Town01 고정 경로 주행 (#15)" 절. 요약은 scripts/analysis/bag_summary.py(AUTO~ARRIVED 구간)
  - 주행 결과: 세 회차 모두 무개입 도착, 중간 정지 0, NVTL 2.3 미만 0건

    | 회차 | goal | AUTO→ARRIVED | 출발 지연 | 이동 시간 | 이동 거리 | 최대/평균 km/h (이동 구간) | NVTL 최소/평균 | goal 오차 | bag |
    |---|---|---|---|---|---|---|---|---|---|
    | A | (397.10, −60.73) yaw 89.54° 직선 190 m | 99.9 s | 35.7 s | 64.3 s | 189.8 m | 13.1/10.6 | 2.57/2.83 | 0.45 m | 15_driveA_1125_1743 |
    | B (RViz 클릭) | (252.83, 2.25) yaw −175.9° | 117.2 s | 11.1 s | 106.1 s | 391.3 m | 16.2/13.3 | 2.58/2.92 | 0.41 m | 15_driveB_1125_1827 |
    | B-cli (고정 goal) | (252.83, 2.25) yaw 180° | 140.5 s | 34.5 s | 106.0 s | 391.3 m | 16.2/13.3 | 2.62/2.89 | 0.44 m | 15_driveB_cli_1125_1839 |

  - 지표 정의(bag_summary.py): 이동 구간 = AUTO 후 첫 이동(속도 ≥0.1 m/s)~ARRIVED. 이동 거리는 이 구간 kinematic_state 위치(x, y) 누적, 속도 최대·평균도 이 구간 기준(처음 기록한 평균 6.8/12.0/10.0 km/h는 출발 지연 정지 시간이 섞인 값이라 PR #24 리뷰에서 수정). NVTL은 AUTO→ARRIVED 전체
  - 출발 지연: 세 회차 모두 Autoware 출발 명령(control_cmd 목표 속도 ≥0.1 m/s)이 AUTO+10.4~34.8 s에 나오고 0.7~0.9 s 뒤 차가 움직임 → 지연은 Autoware 쪽(어느 모듈인지 미확인, planning_factors 비어 있음). #16에서 원인 조사
  - 재현성(같은 goal B): 이동 시간 106.1 s vs 106.0 s, 이동 거리 391.3 m vs 391.3 m, 평균(이동 구간) 13.3 km/h 동일
  - planning_factors: traffic_light·intersection 등이 약 10 Hz로 발행되지만 factor 0건(정지 판단 없음). intersection_collision_checker는 발행 0건. /api/planning/velocity_factors는 goal 정지를 포함해 전 구간 비어 있음
  - 자원(docker stats): 메모리 autoware 정지 9.98 GiB·주행 10.02 GiB, carla 2.51 GiB. CPU 주행 중 carla 212%·autoware 373%. VRAM 정지 6894·주행 6935/16303 MiB, GPU util 36→41%. NET I/O carla→autoware 누적 약 180 GB(센서 스트리밍)
  - VRAM 내역(정지): compute 프로세스는 CARLA 4052 MiB(C+G)·pointcloud_container(centerpoint) 1558 MiB뿐. #14의 CUDA 컨테이너 3×~230 MiB는 재현 안 됨. 그래픽 1089 MiB(Xorg 464, gnome-shell 92, rviz2 301, 기타 앱 2개 232), 미할당 약 195 MiB
