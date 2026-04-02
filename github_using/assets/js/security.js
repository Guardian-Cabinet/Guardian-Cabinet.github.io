/**
 * security.js - GitHub Pages Access Control & Expiry System (Aggressive Mode)
 * 1. 기간 체크
 * 2. 아이디/비번 강제 팝업 (검색 엔진 및 코드 분석 차단 전략)
 */

async function checkAccess() {
    try {
        const response = await fetch('data/config.json');
        if (!response.ok) throw new Error('Config load failed');
        const config = await response.json();
        
        if (!config || !config.settings) return;

        const settings = config.settings;
        const now = new Date();
        const start = new Date(settings.valid_start);
        const end = new Date(settings.valid_end);
        
        // 1. 기간 체크 (ISO Date handling)
        if (now < start || now > end.setHours(23,59,59,999)) {
            window.location.href = 'expired.html';
            return;
        }

        // 2. 인증 체크 (세션 저장소 활용)
        if (settings.allowed_users && settings.allowed_users.length > 0 && !sessionStorage.getItem('portfolio_auth')) {
            // 인증 전에는 화면을 비웁니다.
            document.documentElement.style.display = 'none'; 
            
            const inputId = prompt("👤 보안 접속 아이디(ID)를 입력하세요.");
            if (!inputId) { window.location.href = 'expired.html'; return; }
            
            const inputPin = prompt("🔑 비밀번호(PIN)를 입력하세요.");
            
            const user = settings.allowed_users.find(u => u.id === inputId && u.pin === inputPin);

            if (user) {
                sessionStorage.setItem('portfolio_auth', 'true');
                sessionStorage.setItem('authed_user', user.id);
                document.documentElement.style.display = 'block'; // 인증 성공 시 화면 표시
            } else {
                alert("❌ 접근 권한이 없습니다.");
                window.location.href = 'expired.html';
                return;
            }
        } else {
            // 이미 인증된 상태라면 화면을 표시합니다.
            document.documentElement.style.display = 'block';
        }

        window.portfolioConfig = config;
        document.dispatchEvent(new CustomEvent('securityPassed'));

    } catch (error) {
        console.error('Security Check Error:', error);
    }
}

// 스크립트 실행
checkAccess();
