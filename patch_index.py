import os
import re

file_path = r'g:\다른 컴퓨터\내 컴퓨터_mbc_메인\anti\homepage\portfolio_server\templates\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace CSS
old_css = """        .career-item {
            padding-left: 20px;
            border-left: 3px solid #000;
            margin-bottom: 35px;
            position: relative;
        }
        .career-item::before {
            content: '';
            position: absolute;
            left: -9px;
            top: 0;
            width: 15px;
            height: 15px;
            background: #fff;
            border: 3px solid #000;
            border-radius: 50%;
        }"""
new_css = """        .career-item {
            padding-left: 25px;
            border-left: 3px solid #000;
            margin-bottom: 35px;
            position: relative;
        }
        .timeline-icon {
            position: absolute;
            left: -16px;
            top: -2px;
            width: 30px;
            height: 30px;
            background: #fff;
            border: 3px solid #000;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }"""

content = content.replace(old_css, new_css)

# Replace HTML body
body_pattern = re.compile(r'<!-- 01 PROFILE -->.*?<!-- 06 AWARDS & MILITARY -->.*?{% endif %}', re.DOTALL)
new_body = """<!-- 파셜(Partials)로 모듈화된 폴더 탭 내용들 -->
        {% include 'partials/01_profile.html' %}
        {% include 'partials/02_portfolio.html' %}
        {% include 'partials/03_career.html' %}
        {% include 'partials/04_edu_activities.html' %}
        {% include 'partials/05_skills.html' %}
        {% include 'partials/06_awards_military.html' %}"""

content = body_pattern.sub(new_body, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied to index.html successfully.")
