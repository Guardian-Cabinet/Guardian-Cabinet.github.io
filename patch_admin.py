import os

file_path = r'g:\다른 컴퓨터\내 컴퓨터_mbc_메인\anti\homepage\portfolio_server\templates\admin.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Insight Panel
insight_css = """        .insight-panel { background: #fff3cd; color: #856404; padding: 15px 20px; border-radius: 8px; border-left: 5px solid #ffeeba; margin-bottom: 25px; font-weight: 700; line-height: 1.5; font-size: 15px; }
        .container {"""
html = html.replace('.container {', insight_css)

insight_html = """            <div style="display:flex; gap:10px;">
                <a href="/admin/visits" class="btn" style="background:#0f0f1a; color:#fff; text-decoration:none; padding:8px 15px;">📊 방문자 대시보드</a>
                <a href="/logout" class="btn" style="background:#eee; color:#333; text-decoration:none; padding:8px 15px;">로그아웃</a>
            </div>
        </div>
        {% if insight %}
        <div class="insight-panel">{{ insight }}</div>
        {% endif %}"""
html = html.replace("""            <div style="display:flex; gap:10px;">
                <a href="/admin/visits" class="btn" style="background:#0f0f1a; color:#fff; text-decoration:none; padding:8px 15px;">📊 방문자 대시보드</a>
                <a href="/logout" class="btn" style="background:#eee; color:#333; text-decoration:none; padding:8px 15px;">로그아웃</a>
            </div>
        </div>""", insight_html)

# 2. Add Auto Suggest JS
js_func = """function autoSuggestEmoji(el) {
    const text = el.value || '';
    const arrayItem = el.closest('.array-item');
    if(!arrayItem) return;
    const iconInput = arrayItem.querySelector('.c_icon, .e_icon, .t_icon, .a_icon, .aw_icon, .ce_icon');
    if(!iconInput) return;
    if(iconInput.value.trim() !== '') return;

    let emoji = '';
    if(/개발|코드|프로그래밍|소프트|AI|데이터/i.test(text)) emoji = '👨\\u200d💻';
    else if(/복지|돌봄|센터|봉사|케어/i.test(text)) emoji = '🤝';
    else if(/영상|촬영|편집|PD|유튜브|프리미어|애프터이펙트/i.test(text)) emoji = '🎬';
    else if(/학원|강사|수학|교육|학교/i.test(text)) emoji = '🏫';
    else if(/농사|유기농|재배/i.test(text)) emoji = '🌱';
    else if(/교회|행정/i.test(text)) emoji = '⛪';
    else if(/마케팅|홍보|광고/i.test(text)) emoji = '📢';
    else if(/대상|우수|장려상|장학금/i.test(text)) emoji = '🏆';
    else if(/수료|이수|훈련/i.test(text)) emoji = '📜';
    else if(/자격|면허/i.test(text)) emoji = '🏅';
    else if(/활동/i.test(text)) emoji = '🏃';
    
    if(emoji) {
        iconInput.value = emoji;
    }
}

async function uploadImage"""
html = html.replace('async function uploadImage', js_func)

# 3. Replace HTML forms
html = html.replace(
    '<div style="display:flex; gap:10px; margin-bottom:10px;"><input type="text" class="c_period" value="{{ c.period }}" placeholder="기간"><input type="text" class="c_company" value="{{ c.company }}" placeholder="기관/회사명"></div>',
    '<div style="display:flex; gap:10px; margin-bottom:10px;"><input type="text" class="c_icon" value="{{ c.icon }}" placeholder="아이콘" style="width:100px;" onchange="autoSuggestEmoji(this)"><input type="text" class="c_period" value="{{ c.period }}" placeholder="기간"><input type="text" class="c_company" value="{{ c.company }}" placeholder="기관/회사명" onchange="autoSuggestEmoji(this)"></div>'
)
html = html.replace('<textarea class="c_role" placeholder="담당 업무 및 성과">{{ c.role }}</textarea>', '<textarea class="c_role" placeholder="담당 업무 및 성과" onchange="autoSuggestEmoji(this)">{{ c.role }}</textarea>')

html = html.replace(
    '<input type="text" class="e_period" value="{{ e.period }}"><input type="text" class="e_school" value="{{ e.school }}">',
    '<div style="display:flex; gap:5px;"><input type="text" class="e_icon" value="{{ e.icon }}" placeholder="아이콘" style="width:70px;" onchange="autoSuggestEmoji(this)"><input type="text" class="e_period" value="{{ e.period }}"></div><input type="text" class="e_school" value="{{ e.school }}" onchange="autoSuggestEmoji(this)">'
)
html = html.replace('<textarea class="e_detail">{{ e.detail }}</textarea>', '<textarea class="e_detail" onchange="autoSuggestEmoji(this)">{{ e.detail }}</textarea>')

html = html.replace(
    '<input type="text" class="t_period" value="{{ t.period }}"><input type="text" class="t_title" value="{{ t.title }}">',
    '<div style="display:flex; gap:5px;"><input type="text" class="t_icon" value="{{ t.icon }}" placeholder="아이콘" style="width:70px;" onchange="autoSuggestEmoji(this)"><input type="text" class="t_period" value="{{ t.period }}"></div><input type="text" class="t_title" value="{{ t.title }}" onchange="autoSuggestEmoji(this)">'
)
html = html.replace('<textarea class="t_detail">{{ t.detail }}</textarea>', '<textarea class="t_detail" onchange="autoSuggestEmoji(this)">{{ t.detail }}</textarea>')

html = html.replace(
    '<input type="text" class="a_period" value="{{ a.period }}"><input type="text" class="a_title" value="{{ a.title }}">',
    '<div style="display:flex; gap:5px;"><input type="text" class="a_icon" value="{{ a.icon }}" placeholder="아이콘" style="width:70px;" onchange="autoSuggestEmoji(this)"><input type="text" class="a_period" value="{{ a.period }}"></div><input type="text" class="a_title" value="{{ a.title }}" onchange="autoSuggestEmoji(this)">'
)
html = html.replace('<textarea class="a_detail">{{ a.detail }}</textarea>', '<textarea class="a_detail" onchange="autoSuggestEmoji(this)">{{ a.detail }}</textarea>')

html = html.replace(
    '<input type="text" class="aw_title" value="{{ award.title }}" placeholder="년도/대회명" style="margin-bottom:5px;">',
    '<div style="display:flex; gap:5px;"><input type="text" class="aw_icon" value="{{ award.icon }}" placeholder="아이콘" style="width:70px;" onchange="autoSuggestEmoji(this)"><input type="text" class="aw_title" value="{{ award.title }}" placeholder="년도/대회명" style="margin-bottom:5px;"></div>'
)
html = html.replace('<input type="text" class="aw_date" value="{{ award.date }}" placeholder="수상 내용" style="margin-bottom:5px;">', '<input type="text" class="aw_date" value="{{ award.date }}" placeholder="수상 내용" style="margin-bottom:5px;" onchange="autoSuggestEmoji(this)">')

html = html.replace(
    '<input type="text" class="ce_name" value="{{ cert.name }}" style="flex:2;" placeholder="자격증명">',
    '<input type="text" class="ce_icon" value="{{ cert.icon }}" placeholder="아이콘" style="width:70px;" onchange="autoSuggestEmoji(this)"><input type="text" class="ce_name" value="{{ cert.name }}" style="flex:2;" placeholder="자격증명" onchange="autoSuggestEmoji(this)">'
)

# 4. Update the addItem strings
html = html.replace(
    "case 'career': container = 'career_container'; html = `<div class=\"array-item item-career\"><button type=\"button\" class=\"btn btn-danger\"",
    "case 'career': container = 'career_container'; html = `<div class=\"array-item item-career\"><button type=\"button\" class=\"btn btn-danger\""
)
# Just a safe replace for career_container
old_c = "html = `<div class=\"array-item item-career\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">삭제</button><input type=\"hidden\" class=\"c_id\" value=\"${Date.now()}\"><div style=\"display:flex; gap:10px; margin-bottom:10px;\"><input type=\"text\" class=\"c_period\" placeholder=\"기간\"><input type=\"text\" class=\"c_company\" placeholder=\"회사\"></div><textarea class=\"c_role\"></textarea></div>`;"
new_c = "html = `<div class=\"array-item item-career\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">삭제</button><input type=\"hidden\" class=\"c_id\" value=\"${Date.now()}\"><div style=\"display:flex; gap:10px; margin-bottom:10px;\"><input type=\"text\" class=\"c_icon\" placeholder=\"아이콘\" style=\"width:100px;\" onchange=\"autoSuggestEmoji(this)\"><input type=\"text\" class=\"c_period\" placeholder=\"기간\"><input type=\"text\" class=\"c_company\" placeholder=\"회사\" onchange=\"autoSuggestEmoji(this)\"></div><textarea class=\"c_role\" onchange=\"autoSuggestEmoji(this)\"></textarea></div>`;"
html = html.replace(old_c, new_c)

old_e = "html = `<div class=\"array-item item-edu\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button><input type=\"hidden\" class=\"e_id\" value=\"${Date.now()}\"><input type=\"text\" class=\"e_period\" style=\"margin-bottom:5px;\"><input type=\"text\" class=\"e_school\"><textarea class=\"e_detail\"></textarea></div>`;"
new_e = "html = `<div class=\"array-item item-edu\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button><input type=\"hidden\" class=\"e_id\" value=\"${Date.now()}\"><div style=\"display:flex; gap:5px;\"><input type=\"text\" class=\"e_icon\" placeholder=\"아이콘\" style=\"width:70px;\" onchange=\"autoSuggestEmoji(this)\"><input type=\"text\" class=\"e_period\" style=\"margin-bottom:5px;\"></div><input type=\"text\" class=\"e_school\" onchange=\"autoSuggestEmoji(this)\"><textarea class=\"e_detail\" onchange=\"autoSuggestEmoji(this)\"></textarea></div>`;"
html = html.replace(old_e, new_e)

old_t = "html = `<div class=\"array-item item-train\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button><input type=\"text\" class=\"t_period\" style=\"margin-bottom:5px;\"><input type=\"text\" class=\"t_title\"><textarea class=\"t_detail\"></textarea></div>`;"
new_t = "html = `<div class=\"array-item item-train\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button><div style=\"display:flex; gap:5px;\"><input type=\"text\" class=\"t_icon\" placeholder=\"아이콘\" style=\"width:70px;\" onchange=\"autoSuggestEmoji(this)\"><input type=\"text\" class=\"t_period\" style=\"margin-bottom:5px;\"></div><input type=\"text\" class=\"t_title\" onchange=\"autoSuggestEmoji(this)\"><textarea class=\"t_detail\" onchange=\"autoSuggestEmoji(this)\"></textarea></div>`;"
html = html.replace(old_t, new_t)

old_a = "html = `<div class=\"array-item item-act\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button><input type=\"text\" class=\"a_period\" style=\"margin-bottom:5px;\"><input type=\"text\" class=\"a_title\"><textarea class=\"a_detail\"></textarea></div>`;"
new_a = "html = `<div class=\"array-item item-act\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button><div style=\"display:flex; gap:5px;\"><input type=\"text\" class=\"a_icon\" placeholder=\"아이콘\" style=\"width:70px;\" onchange=\"autoSuggestEmoji(this)\"><input type=\"text\" class=\"a_period\" style=\"margin-bottom:5px;\"></div><input type=\"text\" class=\"a_title\" onchange=\"autoSuggestEmoji(this)\"><textarea class=\"a_detail\" onchange=\"autoSuggestEmoji(this)\"></textarea></div>`;"
html = html.replace(old_a, new_a)

old_aw = "html = `<div class=\"array-item item-award\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button><input type=\"text\" class=\"aw_title\" placeholder=\"년도\" style=\"margin-bottom:5px;\"><input type=\"text\" class=\"aw_date\" placeholder=\"내용\" style=\"margin-bottom:5px;\"><input type=\"text\" class=\"aw_org\" placeholder=\"기관\"></div>`;"
new_aw = "html = `<div class=\"array-item item-award\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button><div style=\"display:flex; gap:5px;\"><input type=\"text\" class=\"aw_icon\" placeholder=\"아이콘\" style=\"width:70px;\" onchange=\"autoSuggestEmoji(this)\"><input type=\"text\" class=\"aw_title\" placeholder=\"년도\" style=\"margin-bottom:5px;\"></div><input type=\"text\" class=\"aw_date\" placeholder=\"내용\" style=\"margin-bottom:5px;\" onchange=\"autoSuggestEmoji(this)\"><input type=\"text\" class=\"aw_org\" placeholder=\"기관\"></div>`;"
html = html.replace(old_aw, new_aw)

old_ce = "html = `<div class=\"array-item item-cert\" style=\"display:flex; gap:10px; align-items:center;\"><input type=\"text\" class=\"ce_name\" style=\"flex:2;\" placeholder=\"자격증명\"><input type=\"text\" class=\"ce_date\" style=\"flex:1;\" placeholder=\"취득일\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button></div>`;"
new_ce = "html = `<div class=\"array-item item-cert\" style=\"display:flex; gap:10px; align-items:center;\"><input type=\"text\" class=\"ce_icon\" placeholder=\"아이콘\" style=\"width:70px;\" onchange=\"autoSuggestEmoji(this)\"><input type=\"text\" class=\"ce_name\" style=\"flex:2;\" placeholder=\"자격증명\" onchange=\"autoSuggestEmoji(this)\"><input type=\"text\" class=\"ce_date\" style=\"flex:1;\" placeholder=\"취득일\"><button type=\"button\" class=\"btn btn-danger\" onclick=\"this.parentElement.remove()\">X</button></div>`;"
html = html.replace(old_ce, new_ce)

# 5. Extraction updates
html = html.replace(
    "out.content.careers.push({ id: el.querySelector('.c_id').value, period: el.querySelector('.c_period').value, company: el.querySelector('.c_company').value, role: el.querySelector('.c_role').value })",
    "out.content.careers.push({ id: el.querySelector('.c_id').value, icon: el.querySelector('.c_icon').value, period: el.querySelector('.c_period').value, company: el.querySelector('.c_company').value, role: el.querySelector('.c_role').value })"
)
html = html.replace(
    "out.content.educations.push({ id: el.querySelector('.e_id').value, period: el.querySelector('.e_period').value, school: el.querySelector('.e_school').value, detail: el.querySelector('.e_detail').value })",
    "out.content.educations.push({ id: el.querySelector('.e_id').value, icon: el.querySelector('.e_icon').value, period: el.querySelector('.e_period').value, school: el.querySelector('.e_school').value, detail: el.querySelector('.e_detail').value })"
)
html = html.replace(
    "out.content.trainings.push({ period: el.querySelector('.t_period').value, title: el.querySelector('.t_title').value, detail: el.querySelector('.t_detail').value })",
    "out.content.trainings.push({ icon: el.querySelector('.t_icon').value, period: el.querySelector('.t_period').value, title: el.querySelector('.t_title').value, detail: el.querySelector('.t_detail').value })"
)
html = html.replace(
    "out.content.activities.push({ period: el.querySelector('.a_period').value, title: el.querySelector('.a_title').value, detail: el.querySelector('.a_detail').value })",
    "out.content.activities.push({ icon: el.querySelector('.a_icon').value, period: el.querySelector('.a_period').value, title: el.querySelector('.a_title').value, detail: el.querySelector('.a_detail').value })"
)
html = html.replace(
    "out.content.awards.push({ title: el.querySelector('.aw_title').value, date: el.querySelector('.aw_date').value, organization: el.querySelector('.aw_org').value })",
    "out.content.awards.push({ icon: el.querySelector('.aw_icon').value, title: el.querySelector('.aw_title').value, date: el.querySelector('.aw_date').value, organization: el.querySelector('.aw_org').value })"
)
html = html.replace(
    "out.content.skills.certs.push({ name: el.querySelector('.ce_name').value, date: el.querySelector('.ce_date').value })",
    "out.content.skills.certs.push({ icon: el.querySelector('.ce_icon').value, name: el.querySelector('.ce_name').value, date: el.querySelector('.ce_date').value })"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch applied to admin.html successfully.")
