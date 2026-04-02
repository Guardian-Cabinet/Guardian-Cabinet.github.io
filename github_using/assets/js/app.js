/**
 * app.js - Content Loading & Dynamic Rendering (v3.0 Final) - Stable Edition
 */

let currentActive = 0;
let portfolioData = null;
let visibilities = {};

// Helper: Handle Newlines in Admin-provided text
const formatTxt = (txt) => txt ? txt.toString().replace(/\n/g, '<br>') : '';

async function initPortfolio() {
    try {
        if (!window.portfolioConfig) {
            await new Promise(resolve => document.addEventListener('securityPassed', resolve));
        }
        visibilities = window.portfolioConfig.settings.visibilities;
        const response = await fetch('data/content.json');
        portfolioData = await response.json();

        renderFolders();
        document.body.style.opacity = "1";
    } catch (error) {
        console.error('Initialization Error:', error);
    }
}

function renderFolders() {
    const cabinet = document.getElementById('folder-container');
    cabinet.innerHTML = '';

    const labels = portfolioData.site_labels || { left: "SECTION", right: "KWON ARCHIVE" };

    const categories = [
        { id: "01 PROFILE", title: "About Me", emoji: "👤" },
        { id: "02 PORTFOLIO", title: "Projects", emoji: "📂" },
        { id: "03 CAREER", title: "Career History", emoji: "💼" },
        { id: "04 EDU & ACTIVITIES", title: "Education", emoji: "🎓" },
        { id: "05 SKILLS & CERTS", title: "Skills", emoji: "🛠️" },
        { id: "06 AWARDS & MILITARY", title: "Honors", emoji: "🎖️" }
    ];

    const activeCategories = categories.filter(cat => visibilities[cat.id]);

    activeCategories.forEach((cat, index) => {
        const folder = document.createElement('div');
        folder.className = 'folder';
        folder.onclick = () => openFolder(index);

        const tabOffset = (index / activeCategories.length) * 85;

        folder.innerHTML = `
            <div class="tab-wrapper">
                <div class="tab ${index === currentActive ? 'tab-active' : ''}" style="left: ${tabOffset}%">
                    ${cat.id} <span style="font-size:1rem;">${cat.emoji}</span>
                </div>
            </div>
            <div class="folder-body">
                <div class="header-frame">
                    <div class="header-cell">${labels.left} 0${index + 1}</div>
                    <div class="header-cell">${cat.id}</div>
                    <div class="header-cell">${labels.right}</div>
                </div>
                <div id="content-${index}"></div>
            </div>
        `;
        cabinet.appendChild(folder);
        injectContent(cat.id, `content-${index}`);
    });

    layoutFolders();
}

function injectContent(catId, targetId) {
    const target = document.getElementById(targetId);
    if (!portfolioData) return;

    let html = "";

    switch(catId) {
        case "01 PROFILE":
            const p = portfolioData.profile;
            html = `<h1 style="color:#111;">${formatTxt(p.title)}</h1>
                    <div class="content-grid">
                        <div class="media-container"><img src="${p.image_url}" onerror="this.src='https://via.placeholder.com/350x350'"></div>
                        <div>
                            <span class="badge">${p.badge_text}</span>
                            <p style="color:#111; font-weight:500;">${formatTxt(p.description)}</p>
                            <hr style="border:0; border-top:3px solid #111; margin:20px 0;">
                            <h3 style="margin-bottom:10px;">CONTACT</h3>
                            <p style="font-weight:700;">📧 Email: ${p.email}</p>
                        </div>
                    </div>`;
            break;

        case "02 PORTFOLIO":
            html = `<div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px;">`;
            portfolioData.portfolio_items.forEach(item => {
                html += `
                    <div class="timeline-content" style="width:100%; box-shadow: 6px 6px 0 #111;">
                        <img src="${item.thumbnail}" style="width:100%; border-radius:8px; border:2.5px solid #111;">
                        <h3 style="margin:15px 0 5px 0;">${item.title}</h3>
                        <p style="font-size:0.9rem; color:#444; margin-bottom:15px;">${formatTxt(item.description)}</p>
                        <a href="${item.url}" target="_blank" style="font-weight:800; color:#111; text-decoration:none; border-bottom:2.5px solid #111; font-size:0.85rem;">VIEW PROJECT →</a>
                    </div>`;
            });
            html += `</div>`;
            break;

        case "03 CAREER":
        case "04 EDU & ACTIVITIES":
            // Render the list in the order provided (user can control order in admin)
            const rawArr = (catId === "03 CAREER") ? (portfolioData.careers || []) : (portfolioData.educations || []);
            html = `<div class="timeline-container">
                        <div class="timeline-line"></div>`;
            rawArr.forEach((c) => {
                if(!c) return;
                const iconHtml = (c.image_url) 
                    ? `<img src="${c.image_url}" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">` 
                    : (c.emoji || (catId === "03 CAREER" ? '💼' : '🎓'));

                html += `
                    <div class="timeline-item">
                        <div class="timeline-dot" style="padding:0; overflow:hidden; background:white;">${iconHtml}</div>
                        <div class="timeline-content">
                            <span style="font-family:'JetBrains Mono'; font-weight:700; color:#777; font-size:0.85rem;">${c.period || ''}</span>
                            <h3 style="margin:8px 0;">${(c.company || c.school || '')}</h3>
                            <p style="font-size:0.9rem; color:#111; margin:0;">${formatTxt(c.role || c.detail || '')}</p>
                        </div>
                    </div>`;
            });
            html += `</div>`;
            break;
            
        case "05 SKILLS & CERTS":
            html = `<h3>TECH STACK</h3>`;
            const techStr = (portfolioData.skills && portfolioData.skills.tech) ? portfolioData.skills.tech : "";
            techStr.split(',').forEach(s => {
                if(s.trim()) html += `<span class="badge" style="margin-right:5px; margin-bottom:5px; display:inline-block;">${s.trim()}</span> `;
            });
            html += `<hr style="margin:30px 0; border:1px dashed #ccc;"><h3>CERTIFICATIONS</h3><ul style="padding-left:20px;">`;
            const certs = (portfolioData.skills && portfolioData.skills.certs) ? portfolioData.skills.certs : [];
            certs.forEach(c => {
                html += `<li style="margin-bottom:8px;"><strong>${c.name}</strong> <span style="color:#666;">(${c.date})</span></li>`;
            });
            html += `</ul>`;
            break;

        case "06 AWARDS & MILITARY":
            html = `
                <div style="padding:15px; background:#f9f9f9; border:2.5px solid #111; margin-bottom:25px; border-radius:10px;">
                    <h3 style="margin-bottom:8px;">MILITARY SERVICE</h3>
                    <p style="font-weight:700; color:#333; margin:0;">🪖 ${portfolioData.military || '기입된 병역 기록이 없습니다.'}</p>
                </div>
                <h3>HONORS & AWARDS</h3><ul style="padding-left:20px;">`;
            (portfolioData.awards || []).forEach(a => {
                html += `<li style="margin-bottom:12px;"><strong>${a.name}</strong> <span style="color:#666;">- ${a.date}</span></li>`;
            });
            html += `</ul>`;
            break;

        default: html = `<p>Ready to customize...</p>`;
    }
    target.innerHTML = html;
}

function layoutFolders() {
    const folders = document.querySelectorAll('.folder');
    const container = document.getElementById('folder-container');
    const n = folders.length;
    if (n === 0 || !container) return;

    const containerHeight = container.clientHeight;
    const padding = 65; 
    const folderHeight = containerHeight - ((n - 1) * padding);

    folders.forEach((folder, i) => {
        folder.style.height = `${folderHeight}px`;
        const body = folder.querySelector('.folder-body');
        if (i === currentActive) {
            folder.style.transform = `translateY(${i * padding}px)`;
            folder.style.zIndex = "10";
            body.style.display = "block";
        } else {
            const offset = (i <= currentActive) ? (i * padding) : (containerHeight - ((n - i) * padding));
            folder.style.transform = `translateY(${offset}px)`;
            folder.style.zIndex = String(i);
        }
    });
}

function openFolder(index) {
    currentActive = index;
    const container = document.getElementById('folder-container');
    container.setAttribute('data-active', index);
    renderFolders();
}

window.addEventListener('resize', layoutFolders);
initPortfolio();
