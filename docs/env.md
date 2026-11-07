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
| Autoware | Docker 이미지 (ROS 2 Humble) | 미설치 | 이미지 태그 기록할 것 |
| CARLA | 0.9.15 | 미설치 | |

## 경로

| 용도 | 경로 |
|---|---|
| 저장소 | `~/Desktop/develop/carla-autoware-lab` |
| CARLA 설치 위치 | (설치 후 기록) |
| Autoware 맵·데이터 | (설치 후 기록) |

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

## 트러블슈팅 기록

형식: 날짜 / 증상 / 원인 / 해결

<!-- 예시
### 2026-11-06 / nvidia-smi에서 GPU가 안 보임
- 원인:
- 해결:
-->
