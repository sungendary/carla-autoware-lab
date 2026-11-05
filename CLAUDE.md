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