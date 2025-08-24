# songecon-rss (비공식)

아이패드만 있어도 깃허브에서 바로 돌고, GitHub Pages로 **구독 가능한 RSS URL**을 배포하는 레포입니다.
- 대상: 이진우의 손에 잡히는 경제, 손경제 플러스, 손경제 상담소
- 소스: iMBC의 날짜 기반 MP3 경로를 확인해 **실재 파일만** RSS에 반영
- 용도: **개인 자동화 용도** (MBC의 사전 동의 없는 영리 목적 사용/재제공 금지)

## 사용법 (아이패드로도 가능)
1. 이 레포 구조를 그대로 새 레포에 업로드
2. `Settings → Pages → Build and deployment`에서 **Source: GitHub Actions** 선택
3. `Actions` 탭에서 워크플로(빌드+배포) 허용
4. 배포가 끝나면 Pages URL: `https://<username>.github.io/<repo>/rss_songecon.xml`

## 스케줄
- 평일 오전 07:05 (Asia/Seoul) 기준으로 실행되도록 UTC(전날 22:05)로 크론 설정

## 로컬/수동 테스트
Actions에서 `Run workflow` 눌러 수동 실행 가능.

## 면책
- 이 피드는 **비공식**이며, 개인적 용도에 한정하세요.
- 상표/저작권은 각 소유자에게 있습니다.
