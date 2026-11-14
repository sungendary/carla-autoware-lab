# Decisions

> 이 파일은 "왜 그렇게 정했는지"를 담는다.
> 선택지가 있었던 결정만 짧게 남긴다. 나중에 "왜 이렇게 설계했는가"를 설명하는 근거가 된다.

형식
- 날짜 / 결정 / 배경 / 고려한 대안 / 이유 / 다시 볼 조건

---

## D-001. Ubuntu 24.04를 유지하고 Autoware는 Docker(Humble)로 실행

- 날짜: 2026-11-05
- 배경: 내 PC는 Ubuntu 24.04인데, CARLA 연동 패키지(autoware_carla_interface)의 공식 지원 환경은 Ubuntu 22.04 + ROS 2 Humble + CARLA 0.9.15다. 2026-11-15 재확인: 공식 Autoware 이미지는 Humble·Jazzy 모두 제공되고 Open AD Kit carla-interface 이미지도 양쪽 배포되지만, Open AD Kit CARLA 배포는 Humble 전용이다. Humble 유지.
- 고려한 대안
  - Ubuntu 22.04로 재설치
  - Ubuntu 24.04 + ROS 2 Jazzy로 바로 진행
- 이유: 재설치 없이 문서 기준 조합(Humble)을 컨테이너로 맞출 수 있다. Jazzy 연동은 아직 검증 사례가 적어 초반에 막힐 위험이 크다.
- 다시 볼 조건: CARLA 연동이 Jazzy에서 공식 지원되거나, Humble 컨테이너에서 해결 못 할 문제가 생길 때

## D-002. CARLA는 0.9.16 사용, 서버는 Docker로 실행 (0.9.15·0.10 아님)

- 날짜: 2026-11-07 (최초 2026-11-05 0.9.15로 결정 → 변경)
- 배경: Autoware 위키 기준 커뮤니티 유지 버전은 0.9.16(UE4)과 0.10.0(UE5)이다. autoware_carla_interface 문서는 0.9.15로 표기되어 있지만 0.9.16에서도 수정 없이 동작한다. Open AD Kit의 CARLA E2E 데모는 carlasim/carla:0.9.16 + Town01 구성이다. 이 데모는 모듈형 구성(서비스별 컨테이너, network_mode: host)이고 Town01 자산을 carla-simulator/autoware-contents 고정 커밋 + sha256으로 받는다. 호스트 요구는 Ubuntu 22.04. CARLA는 Ubuntu 24.04를 내부 테스트하지 않는다(권장 최대 22.04).
- 고려한 대안: 0.9.15(기존 결정), 0.10.0, 호스트에 바이너리 직접 설치
- 이유: Phase 1 목표(Town01 E2E)와 공식 데모 구성이 같다. 0.10은 Autoware 브리지 지원이 미확인이다. 서버를 Docker로 돌리면 24.04 미테스트 문제를 피하고, 호스트에는 Python 클라이언트(conda env carla, Python 3.10)만 둔다. Autoware Humble 컨테이너와 Python 버전을 맞추고 시스템 패키지 설치를 피하기 위함.
- 다시 볼 조건: RTX 5070 Ti/595 드라이버에서 컨테이너 렌더링이 해결되지 않을 때, 또는 Autoware가 0.10을 공식 지원할 때

## D-003. 도구 역할 분담: 저장소가 원본, Project는 사본

- 날짜: 2026-11-05
- 배경: 장기 프로젝트에서 Claude Project, GitHub, Claude Code를 함께 쓴다.
- 결정
  - GitHub 저장소: 코드와 기록의 원본
  - Claude Project: 계획, 개념 학습, 회고 (지식 파일은 저장소의 사본)
  - Claude Code: 로컬 PC에서 구현과 디버깅
- 이유: 기록을 한 곳에 모아야 오래된 정보가 섞이지 않고, 진행 과정이 그대로 추적 가능한 기록으로 남는다.
- 다시 볼 조건: 주간 동기화가 너무 번거로워질 때

## D-004. 브랜치 전략: GitHub Flow + 버전 태그 (Git Flow 아님)

- 날짜: 2026-11-05
- 배경: 실무 방식의 버전 관리를 적용하려 한다.
- 고려한 대안: Git Flow(main, develop, feature, release, hotfix), 인지·판단·제어 모듈별 장기 브랜치
- 이유: 혼자 진행하고 배포·구버전 유지 대상이 없어 Git Flow는 과하다. 모듈은 폴더로 나누고 브랜치는 이슈 단위로 짧게 쓴다. 버전 확정은 Phase 완료 시 태그(v0.1.0 등)로 한다.
- 다시 볼 조건: 협업자가 생기거나 여러 버전을 동시에 유지해야 할 때

## D-005. DevOps는 환경 재현과 자동 검증에 집중

- 날짜: 2026-11-05
- 배경: 모듈이 많아 한 곳의 변경이 다른 곳을 망가뜨리기 쉽다.
- 고려한 대안: 운영 중심 DevOps(클라우드 배포, 쿠버네티스)
- 이유: 배포 대상이 없어 운영 DevOps는 과하다. Docker 버전 고정, CI(빌드·테스트), 시뮬레이션 회귀 테스트를 Phase에 맞춰 단계적으로 도입한다. 실제 불편함이 생길 때 도입하고 전체 시간의 20% 이내로 유지한다.
- 다시 볼 조건: 도구 유지보수가 본 작업 시간을 크게 잡아먹을 때

## D-006. 문서의 사소한 수정은 main에 직접 커밋 허용

- 날짜: 2026-11-06
- 배경: 체크 표시·오타 수정 같은 작은 변경에도 브랜치·PR·삭제 과정을 반복하는 비용이 크다.
- 고려한 대안: 모든 변경을 브랜치로 진행(D-004 유지), 사소한 수정을 모아 주간 회고 PR에 포함
- 이유: 실행에 영향을 줄 수 없는 문서 수정은 "main은 항상 실행 가능" 원칙을 해치지 않는다. 기준을 명시해 예외가 넓어지는 것을 막는다.
- 다시 볼 조건: 직접 커밋한 변경 때문에 문제가 생기거나, 협업자가 생길 때

## D-007. Autoware 컨테이너는 기본 bridge 네트워크 + NET_ADMIN, 호스트 rmem_max는 영구 상향

- 날짜: 2026-11-07
- 배경: Autoware 이미지의 CycloneDDS 설정은 lo 전용 + multicast + 수신 버퍼 최소 10MB를 요구한다. lo multicast 설정에 NET_ADMIN 권한이 필요했고, 호스트 net.core.rmem_max(커널 기본 4MB) 때문에 launch가 즉시 실패했다.
- 고려한 대안
  - --net host + 호스트 lo multicast 변경
  - cyclonedds.xml을 수정해 버퍼 최소값을 낮춰서 마운트
  - 부팅할 때마다 sudo sysctl -w로 적용
- 이유: 컨테이너 하나로 끝나는 단계에서는 호스트 네트워크 인터페이스를 바꿀 필요가 없다. 공식 DDS 설정을 유지해야 점군 같은 큰 메시지의 손실 위험을 피할 수 있다. rmem_max는 상한일 뿐이라 메모리를 미리 잡지 않으므로, 영구 상향(Autoware 공식 권장값)의 부작용이 작다.
- 다시 볼 조건: Autoware 노드를 여러 컨테이너로 분리해 컨테이너 간 DDS 통신이 필요할 때 (예: Open AD Kit 모듈형은 host 네트워크 사용, D-009)

## D-008. GitHub 인증은 GitHub CLI(gh, 공식 apt 저장소) + HTTPS

- 날짜: 2026-11-08
- 배경: HTTPS + 개인 액세스 토큰을 push마다 입력했고, Claude Code 세션은 push·PR을 할 수 없어 이슈 마무리(템플릿 5)를 사용자가 대신했다.
- 고려한 대안
  - SSH 키: push는 해결되지만 PR·Release 생성은 웹에서 해야 함
  - 토큰을 credential.helper store로 저장: 토큰이 평문 파일(~/.git-credentials)에 남음
  - Ubuntu 기본 저장소의 gh: 버전이 오래되어 최신 명령·수정이 빠짐
- 이유: 한 번의 브라우저 로그인으로 git push 인증과 PR·태그·Release 생성을 CLI에서 처리할 수 있다. 토큰은 시스템 키링에 저장되고, git 인증 도우미는 github.com에만 적용된다. Code 세션도 같은 사용자 인증을 쓰므로 템플릿 5를 끝까지 수행할 수 있다. workflow 권한이 있어 CI 도입(D-005) 때 그대로 쓸 수 있다.
- 다시 볼 조건: 토큰 권한 범위를 줄여야 할 때, 또는 협업자가 생겨 브랜치 보호·리뷰 규칙이 필요할 때

## D-009. CARLA ↔ Autoware 연결: Autoware 단일 이미지 안에서 인터페이스 실행 + 사용자 정의 bridge 네트워크

- 날짜: 2026-11-15
- 배경: universe-cuda-humble-2.0.0에 autoware_carla_interface(autoware_universe 0.53.1)와 carla_sensor_kit_description/launch가 포함되고, e2e_simulator.launch.xml이 simulator_type:=carla를 지원한다(기본값 awsim). 인터페이스는 CARLA Python 클라이언트로 서버에 TCP 접속한다(2000 RPC, 2001 센서 스트리밍).
- 결정
  - 인터페이스는 Autoware 컨테이너 안에서 e2e_simulator로 실행한다.
  - CARLA와 Autoware 컨테이너를 사용자 정의 bridge 네트워크 carla-aw에 연결하고 컨테이너 이름 carla로 접속한다: e2e_simulator 인자 `host:=carla`(기본 localhost), `port:=2000`(기본 2000). e2e_simulator는 인터페이스 launch를 인자 전달 없이 include하므로 최상위에서 준 host·port가 그대로 전달된다.
  - 호스트 공개는 127.0.0.1:2000-2002를 유지한다(호스트 conda 클라이언트용).
  - DDS는 Autoware 컨테이너 내부 lo에서 끝난다(D-007 유지).
- 고려한 대안
  - (B) Open AD Kit 모듈형(openadkit c7586a131cae7dae8c8fa2daf96c3bc7814ca6dd): 서비스별 컨테이너, 전 서비스 network_mode: host, 자체 cyclonedds.xml 마운트
  - (C) 두 컨테이너 모두 --net host
- 이유: Phase 0에서 검증한 이미지와 DDS 설정을 그대로 쓰고, DDS가 컨테이너 밖으로 나가지 않아 호스트 네트워크를 바꿀 필요가 없다. 사용자 정의 네트워크는 이름 해석(DNS)을 제공하고 컨테이너 간 포트를 호스트에 공개하지 않아도 된다. B는 공식 검증 구성이지만 host 네트워크로 D-007이 피한 호스트 인터페이스 공유와 포트 전면 노출이 생기고, 2.0.0과 다른 이미지 버전이 섞인다. 단, CARLA 이미지 digest(aaf1df22…bae953)와 Town01 자산 출처는 B와 같다.
- 다시 볼 조건: 인터페이스나 인지를 별도 컨테이너로 분리해야 할 때, 또는 사용자 정의 네트워크에서 2001 스트리밍·이름 해석 문제가 해결되지 않을 때

## D-010. 컨테이너 안의 CARLA Python 패키지: PyPI 휠 압축 해제 + PYTHONPATH 읽기 전용 마운트

- 날짜: 2026-11-15
- 배경: 2.0.0 이미지에 carla 모듈이 없고(Python 3.10.12), pip도 없다. carla 0.9.16 휠은 Python 의존성(Requires)이 없다.
- 결정: carla-0.9.16-cp310-cp310-manylinux_2_31_x86_64.whl (sha256 52b1f2fafb0655e25954f9f6d1e97c211a4da404217fd1d0094b4b7350737c95)을 ~/autoware_data/python/carla-0.9.16-site에 압축 해제하고 `-v ...:/opt/carla-py:ro`, `-e PYTHONPATH=/opt/carla-py`로 쓴다. ROS 소싱 후에도 PYTHONPATH 유지, import carla 성공 확인.
- 고려한 대안
  - 실행할 때마다 pip 설치: 이미지에 pip 없음, 매번 네트워크 필요
  - 호스트 conda env site-packages 마운트: Python 3.10.22/3.10.12 혼용, 경로 의존
  - digest 고정 파생 이미지: Dockerfile·이미지 관리 부담, apt python3-pip 버전 비고정
- 이유: 해시 하나로 고정되고 이미지를 새로 만들지 않는다. import 시 libcarla 확장 모듈까지 로드되어 공유 라이브러리 문제도 없음을 확인했다.
- 다시 볼 조건: 이미지의 Python 버전이 바뀌거나, 컨테이너에 다른 패키지 추가가 필요해 파생 이미지가 필요해질 때
