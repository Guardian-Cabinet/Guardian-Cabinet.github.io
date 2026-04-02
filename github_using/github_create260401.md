# GitHub Pages 포트폴리오 구축 및 배포 계획서 (2026-04-01)

현재 Render 서버(`https://portfolio23-k7x2.onrender.com/`)의 느린 초기 로딩 속도 문제를 해결하기 위해, 정적 웹 호스팅 서비스인 **GitHub Pages**로 포트폴리오를 이전하기 위한 세부 계획입니다.

---

## 1. 개요 및 목적
*   **목적:** GitHub Pages의 전역 CDN을 활용하여 전 세계 어디서나 수 초 내에 로딩되는 초고속 포트폴리오 환경 구축.
*   **핵심:** 기존의 '파일 캐비닛' 디자인과 전체 기능을 100% 유지하면서 서버 사이드 로직(Python/Render)을 정적(Static) 환경으로 최적화.

## 2. 주요 구성 및 전환 전략

### ① 정적 파일 최적화 (Static Transformation)
*   **기존 방식:** Render 서버에서 Python(Flask/FastAPI)이 템플릿을 렌더링.
*   **전환 방식:** 모든 데이터와 디자인을 포함한 **단일 `index.html`** 파일로 빌드하여 배포. (서버 응답 대기 시간 제거)

### ② 기능 및 디자인 유지 (All-In-One UI)
*   **디자인:** `162131.png` 레퍼런스의 블랙 테마와 탭 스타일 적용.
*   **기능:** `03 CAREER`의 타임라인 인포그래픽(`161142.png` 스타일) 및 폴더 슬라이딩 애니메이션 유지.
*   **이모티콘:** HTML/JS 상단부의 `CONFIG` 변수를 통해 코드 수정 없이 이모티콘 일괄 변경 가능하도록 구조화.

### ③ Admin 및 동적 데이터 처리 (Hybrid Concept)
GitHub Pages는 서버 코드를 실행할 수 없으므로 다음 두 가지 방법 중 하나를 선택합니다:
*   **방법 A (완전 정적):** 관리자 페이지(Admin)에서 수정한 내용을 `data.json` 파일로 저장하고, GitHub Pages가 이 파일을 읽어 화면을 구성.
*   **방법 B (API 연동):** 기존 Render 서버를 **API 전용**으로 두고, GitHub Pages(Frontend)에서 데이터를 비동기로 호출 (디자인과 무거운 자산은 GitHub에서 즉시 로딩).

## 3. 상세 실행 단계 (Workflow)

1.  **Local Build:** 현재의 프로젝트를 GitHub Pages 호환 구조(`index.html`, `assets/`, `data.json`)로 로컬에서 정리.
2.  **Emoji/Config Setup:** 사용자가 쉽게 커스텀할 수 있도록 설정 변수 분리.
3.  **GitHub Repo 생성:** `[username].github.io` 또는 전용 프로젝트 저장소 생성.
4.  **Deployment:** Git을 통한 파일 푸시 및 GitHub Pages 설정 활성화.
5.  **Speed Test:** Lighthouse 등을 통한 로딩 성능 검증.

---

## 4. 기대 효과
*   **로딩 속도:** 5~10초 이상 걸리던 초기 진입 속도를 **1초 내외**로 단축.
*   **유지 보수:** GitHub 저장소에 푸시만 하면 자동으로 업데이트되는 편리한 배포 환경.
*   **비용:** GitHub Pages를 통한 무료 고성능 호스팅.

> **[!IMPORTANT]**  
> 위 계획서 내용을 확인하신 후, 진행을 승인해 주시면 바로 최적화된 `index.html` 파일 제작 및 GitHub 배포를 위한 가이드를 시작하겠습니다.
