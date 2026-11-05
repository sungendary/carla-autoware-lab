# Roadmap

> 이 파일은 프로젝트의 큰 방향과 Phase별 완료 기준을 담는다.
> 자주 바뀌지 않으며, Phase를 넘어갈 때만 다듬는다.

## 프로젝트 목표

CARLA + Autoware로 자율주행의 인지 → 판단 → 제어 파이프라인 전체를 직접 경험하고,
그중 일부 모듈을 직접 구현해 정량적으로 평가한다.

- 목적: 자율주행 SW 직무 관련 역량을 쌓는다 (인지·판단·제어 전반의 이해, 시스템 통합, 정량 평가 경험)
- 결과물 형태: GitHub 저장소 + 데모 영상 + 정량 지표

## Phase 개요

| Phase | 이름 | 상태 |
|---|---|---|
| 0 | 기본기 | 진행 중 |
| 1 | 연동 | 대기 |
| 2 | 모듈 교체 | 대기 |
| 3 | 검증 | 대기 |

## Phase 0 – 기본기

CARLA와 Autoware를 각각 따로 실행할 수 있는 환경을 갖춘다.

완료 기준
- GPU(RTX 5070 Ti)와 Docker 컨테이너 내 GPU 인식 확인
- Autoware planning simulator 실행 성공
- CARLA 단독 실행 및 Python API로 차량 스폰 성공

함께 익힐 것
- ROS 2 기본: 노드, 토픽, TF2, launch, rosbag
- Docker 기본: 이미지, 컨테이너, 볼륨, GPU 연결
- Autoware 구조: sensing → localization → perception → planning → control

## Phase 1 – 연동

CARLA와 Autoware를 연결해 E2E 자율주행을 구동한다.

완료 기준
- CARLA Town01에서 Autoware로 목적지까지 3회 연속 무개입 주행
- 실행 방법을 docs/env.md에 정리해 재현 가능하게 만들기

## Phase 2 – 모듈 교체

인지·판단·제어 중 하나의 모듈을 직접 구현해 교체한다.

완료 기준
- 직접 구현한 모듈 1개를 파이프라인에 연결
- 기본 모듈과 동일 조건에서 정량 비교한 결과 표 작성

후보 (Phase 2 진입 시 하나 선택)
- 제어: Pure Pursuit / Stanley / MPC 구현 후 Autoware 기본 컨트롤러와 비교
- 인지: CARLA 데이터로 3D 객체 검출 모델 학습 후 Autoware 인지 모듈 대체
- 측위: GNSS + IMU EKF 구현 후 오차 비교

## Phase 3 – 검증

시나리오 기반으로 시스템을 반복 평가한다.

완료 기준
- 시나리오 반복 테스트 자동화
- 결과 리포트(지표, 실패 사례 분석) 작성

## 평가 원칙

정량 지표를 낼 때 지킬 규칙.

1. 비교 대상은 외부에서 가져온다 (Autoware 기본 모듈, 교과서 알고리즘, 논문 수치)
2. 지표는 표준 정의를 쓴다 (횡방향 오차 RMS, mAP, Route Completion 등)
3. 같은 맵·경로·속도·시드로 여러 번 반복하고 평균과 표준편차를 보고한다
4. 나빠진 점(트레이드오프)과 시뮬레이션의 한계도 함께 적는다
