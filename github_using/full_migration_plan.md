# GitHub Full Migration & Security Plan (2026-04-01)

기존 `portfolio_server` 기능을 GitHub Pages 기반으로 완벽하게 이식하고, 보안 기능(보여줄 자료 선택, 기간 한정 접속)을 강화하기 위한 전체적인 마이그레이션 계획입니다.

---

## 1. 프로젝트 목표 및 핵심 기능
*   **목표:** 고성능(정적 호스팅) + 고기능(방문자 추적, 관리자 제어, 보안 액세스) 통합.
*   **핵심 보안 사항:**
    1.  **세분화된 자료 제어 (Granular Visibility):** 각 프로젝트, 섹션 단위로 체크박스를 두어 노출 여부 결정.
    2.  **접속 기간 설정 (Time-Limited Access):** 관리자가 정한 기간 내에만 접속 가능 (기간 종료 시 ‘접근 만료’ 페이지로 자동 리다이렉트).
    3.  **프라이빗 데이터 암호화:** 민감한 정보는 클라이언트 사이드 암호화(Access Key 방식)를 적용하여 보호.

## 2. 파일 구조 설계 (`C:\anti\homepage\github_using`)

```
/github_using
├── index.html            # 메인 포트폴리오 (액세스 제어 및 렌더링 로직 포함)
├── expired.html          # 기간 만료 또는 비공개 시 보여줄 안내 페이지
├── admin.html            # 로컬 관리자 도구 (설정 및 데이터 JSON 생성용)
├── assets/
│   ├── css/              # 파일 캐비닛 테마 및 타임라인 스타일
│   ├── js/
│   │   ├── app.js        # 초기 로딩 시 보안/기간 체크 및 렌더링 로직
│   │   ├── security.js   # 암호화 및 유효성 검사 로직
│   │   └── admin_tool.js # 관리자 페이지 전용 로직
│   └── images/           # 각종 미디어 자산
└── data/
    ├── config.json       # 접속 가능 기간, 자료별 노출 여부(Checkboxes) 설정
    └── content.json      # 암호화되거나 정리된 포트폴리오 원본 내용
```

## 3. 보안 및 제어 상세 설계

### ① 세분화된 체크박스 제어 (Visibility Matrix)
*   `config.json`에 각 항목별 `isVisible` 플래그를 저장합니다.
*   예: `PROFILE: { isVisible: true, email: true, phone: false }`, `PROJECT_A: { isVisible: true }`
*   `app.js`에서 이 설정을 읽어 `false`인 항목은 DOM에서 아예 생성하지 않거나 삭제합니다.

### ② 기간 설정 및 자동 차단 (Time-Bomb Logic)
*   `config.json`에 `startDate`, `endDate` (ISO 형식)를 설정합니다.
*   접속 시 `app.js`가 현재 시각을 확인:
    *   `CurrentTime < StartDate` 또는 `CurrentTime > EndDate` 이면 `expired.html`로 즉시 리다이렉트.

### ③ 방문자 추적 (Visits Tracking)
*   서버(Python)가 없어도 **Firebase Realtime Database** (무료)를 사용하여 방문자의 IP(부분), 접속 시간, 페이지 뷰를 100% 자바스크립트로 기록합니다.

## 4. 마이그레이션 단계 (Action Items)

1.  **[Stage 1] 기존 코드 분석:** `portfolio_server`의 Jinja2 템플릿과 `main.py`의 비즈니스 로직을 JS 기반으로 변환 설계.
2.  **[Stage 2] 보안 대시보드 구축:** `admin.html`을 먼저 만들어 기간 설정 및 세분화된 체크박스를 쉽게 조작할 수 있는 UI 구현.
3.  **[Stage 3] 정적 파일 생성:** 디자인(캐비닛, 타임라인)을 포함한 `index.html` 완성.
4.  **[Stage 4] 데이터 통합:** 기존 포트폴리오 내용을 `content.json`으로 정리하여 주입.
5.  **[Stage 5] 배포:** GitHub에 푸시하여 최종 기능 및 보안 검토.

---

> **[!TIP]**  
> 정적 웹의 특성상 완전한 100% 보안(서버측 차단)은 불가능하지만, **JS 난독화와 Access Key(비밀번호) 방식**을 결합하여 일반적인 사용자가 우회하기 매우 어렵도록 견고하게 구축할 것입니다.

**계획서가 마음에 드신다면, `github_using` 폴더에 파일 구조 생성을 시작할까요?**
