# Phase 0 – 기본기: 환경 구성 (2026-11-05 ~ 2026-11-08)

## 목표와 결과

| 완료 기준 (roadmap.md) | 결과 |
|---|---|
| GPU(RTX 5070 Ti)와 Docker 컨테이너 내 GPU 인식 | 호스트·컨테이너 nvidia-smi 확인, 컨테이너 내 OpenGL(rviz2) 렌더링 확인 |
| Autoware planning simulator 실행 | P → G → AUTO 후 목적지 도착(routing/state 3) |
| CARLA 단독 실행 및 Python API로 차량 스폰 | Town01 동기 모드 + 시드 42로 스폰·오토파일럿 주행, 결과 재현 |

실행 방법은 [env.md](../env.md), 버전 선택 이유는 [decisions.md](../decisions.md) 참고. 이 문서에는 명령을 다시 적지 않는다.

## 한 일

- #1 NVIDIA 드라이버: nvidia-driver-595-open(Ubuntu 공식 noble-updates/restricted), 커널 모듈은 DKMS 빌드 + MOK 서명. 프로젝트 전에 580 → 580-open → 595-open으로 바꾼 이력이 있어, 11-06에 구 커널(-30, -31)용 580-open 모듈을 정리했다
- #2 Docker 29.9.0 + NVIDIA Container Toolkit 1.20.1: 2026-09에 설치해 둔 것을 확인하고 기록했다. nvidia 런타임은 기본 런타임이 아니므로 --gpus all이 필요하다
- #3 Autoware universe-cuda-humble-2.0.0: digest로 고정하고 planning simulator를 실행했다. CycloneDDS 요구사항 때문에 bridge 네트워크 + NET_ADMIN, 호스트 rmem_max 영구 상향으로 정했다(D-007)
- #4 CARLA 0.9.16: 서버는 Docker, 클라이언트는 conda env(Python 3.10)로 구성했다(D-002). 동기 모드(0.05 s) + TM 시드 42로 결과를 재현했다
- #5 재현 문서화: apt 기록으로 드라이버·Docker·Toolkit·Miniconda 설치 절차를 복원해 env.md에 추가하고, 이미지 pull을 digest 기준으로 바꿨다. 새 터미널에서 env.md만 보고 실행하는 콜드 런을 했고, Docker 디스크를 점검했으며, GitHub CLI 인증을 도입했다(D-008)

## 막힌 점과 해결

자세한 내용은 env.md 트러블슈팅 참고.

| 증상 | 원인 | 해결 |
|---|---|---|
| 컨테이너 시작 시 lo multicast 설정 실패 경고 | 컨테이너에 NET_ADMIN 권한 없음 | --net host 대신 bridge + --cap-add=NET_ADMIN |
| launch 즉시 socket receive buffer 오류 | 호스트 rmem_max 4MB < DDS 요구 10MB | /etc/sysctl.d로 영구 상향 |
| venv 생성 실패(ensurepip) | 24.04 시스템 Python에 venv 패키지 없음 | 시스템 패키지 대신 conda env(Python 3.10) |
| 콜드 런 중 spawn 스크립트 No such file | env.md에 cd 명령이 없고 주석만 있었음 | cd 줄 추가 |
| grep "<!--" 패턴이 다른 문자열로 바뀜 | 큰따옴표 안에서도 bash 히스토리 확장(!) 발생 | 작은따옴표 사용 |

## 배운 점

- 컨테이너는 호스트 커널의 한계를 그대로 따른다. DDS 수신 버퍼처럼 커널 파라미터가 필요한 설정은 컨테이너 안이 아니라 호스트에서 바꿔야 한다
- 권한은 필요한 만큼만 준다. --net host는 호스트 네트워크 전체를 바꾸지만, NET_ADMIN은 컨테이너 자신의 네트워크만 다룬다
- 태그는 다른 이미지를 가리키도록 바뀔 수 있고, digest는 내용 자체를 가리킨다. digest로 pull한 이미지는 로컬에 태그가 없으므로 docker tag로 이름을 붙여야 run이 그 이미지를 쓴다
- Secure Boot에서 DKMS 모듈은 로컬 MOK 키로 서명된다. 커널이 업데이트되면 dkms status로 새 커널용 빌드를 확인한다
- 동기 모드 + 시드 고정이 재현 가능한 실험의 출발점이고, 기준값을 숫자로 남겨야 나중에 달라졌는지 판단할 수 있다
- docker system df의 RECLAIMABLE은 "실행 중인 컨테이너가 쓰지 않는 용량"일 뿐이다. 정지 중인 프로젝트 이미지도 포함된다
- 문서가 맞는지는 읽어서가 아니라, 문서만 보고 실행해서(콜드 런) 검증한다

## 기준값

- CARLA VRAM(GUI·기본 품질): 기준 481 MiB → Town01 4846 MiB, Town10HD 6989 MiB / 총 16303 MiB
- CARLA 스폰(시드 42, Town01, 60 s): x=396.0, y=249.4 / 이동거리 333.7 m
- Docker 이미지: Autoware 22.8GB, CARLA 29.4GB (루트 파티션 여유 1.1TB)

## 회고

잘된 점
- 버전 선택마다 근거를 남겨, 재설치 없이 Docker로 문서 기준 조합을 맞췄다
- digest·시드·측정값으로 재현성을 숫자로 확보했다
- 임시방편 대신 원인을 해결했다(rmem_max 영구 설정, 필요한 권한만 추가)
- 콜드 런으로 기억에 의존하던 단계를 찾아냈다

개선할 점
- 설치 명령을 나중에 apt 기록으로 복원했다 → 설치하는 그 자리에서 env.md에 적는다
- #4의 재현성을 "동일"이라고만 적었다 → 기준값은 숫자로 남긴다
- 자리표시를 채우지 않은 프롬프트를 보냈다 → prompts.md에 확인 문구를 추가했다
- GPU CUDA 연산은 아직 검증하지 않았다 → Phase 2 진입 전에 확인한다

## Phase 1로 넘기는 것

- D-007 재검토: CARLA 브리지가 Autoware와 다른 컨테이너(네트워크 네임스페이스)에서 DDS로 통신해야 함. 현재 DDS 설정은 lo 전용
- CARLA 포트 127.0.0.1 바인딩: 브리지 연결 방식에 따라 재검토
- D-001: CARLA 인터페이스의 Jazzy 지원 여부 재확인
- VRAM: CARLA(Town01 약 4.3GB)와 Autoware를 동시에 실행할 때 사용량 측정
- graphics-drivers PPA: 등록되어 있으나 미사용. apt upgrade 때 드라이버 출처가 바뀌지 않는지 확인
