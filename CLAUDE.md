# Project: carla-autoware-lab
CARLA + Autoware로 인지-판단-제어 파이프라인을 학습하는 개인 프로젝트.

## 환경
- Host: Ubuntu 24.04, RTX 5070 Ti, NVIDIA driver 570+
- Autoware: Docker (ROS 2 Humble, universe-cuda 이미지)
- CARLA: 0.9.15
- 자세한 버전과 명령은 docs/env.md 참고

## 작업 규칙
- 시스템 설정 변경(드라이버, apt 대량 설치 등) 전에는 반드시 나에게 먼저 물어볼 것
- 설치·오류 해결 과정은 docs/env.md 또는 troubleshooting에 기록할 것
- 커밋 메시지: `[label] 무엇을 했는지` (예: `[setup] Docker GPU 확인`)
- 설명은 한국어로

## 브랜치·커밋 규칙 (GitHub Flow)
- main은 항상 실행 가능한 상태로 유지한다. main에 직접 커밋하지 않는다
- 이슈마다 브랜치를 만든다: 종류/영역-주제 (feat/, fix/, exp/, docs/, setup/)
  예: setup/docker-gpu, feat/control-pure-pursuit
- 작업이 끝나면 PR을 만들고, 본문에 무엇을·왜·어떻게 확인했는지와 `Closes #번호`를 적는다
- Phase 완료 시 main에 버전 태그를 붙인다 (Phase 0 → v0.1.0)

## 답변 형식

작업 관련 답변의 끝에는 docs/prompts.md의 형식으로 [작업 상태] 블록을 작성해라.