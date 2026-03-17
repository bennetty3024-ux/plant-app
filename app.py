<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>나만의 정원 매니저 v3.0</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f4f9f4; margin: 0; padding: 20px; color: #333; }
        h1 { color: #2e7d32; text-align: center; }
        .card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        label { font-weight: bold; display: block; margin-top: 10px; color: #555; }
        input[type="text"], select, textarea { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        .checkbox-group { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 5px; }
        .checkbox-group label { font-weight: normal; display: flex; align-items: center; margin-top: 0; }
        .checkbox-group input { margin-right: 5px; }
        button { background-color: #4caf50; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-size: 16px; width: 100%; margin-top: 15px; }
        button:hover { background-color: #45a049; }
        .plant-item { border-left: 5px solid #4caf50; padding-left: 15px; margin-bottom: 20px; background: #fafafa; padding: 15px; border-radius: 8px; }
        .plant-name { font-size: 1.2em; font-weight: bold; color: #2e7d32; }
        .tips { background: #e8f5e9; padding: 10px; border-radius: 6px; margin-top: 10px; font-size: 0.9em; }
        .warning { color: #d32f2f; font-weight: bold; }
        .calendar-btn { background-color: #4285F4; margin-top: 10px; }
        .hidden { display: none; }
    </style>
</head>
<body>

    <h1>🌿 나만의 정원 매니저 v3.0</h1>

    <div class="card">
        <h3>새 식물/작업 등록</h3>
        <label>식물 이름 (개체별)</label>
        <input type="text" id="plantName" placeholder="예: 스카푸 1호, 금어초 파종이">

        <label>현재 단계</label>
        <select id="plantStage" onchange="toggleRepottingFields()">
            <option value="파종">파종</option>
            <option value="정식" selected>정식 (분갈이)</option>
            <option value="성장">성장</option>
            <option value="개화">개화</option>
        </select>

        <div id="repottingFields">
            <label>화분/흙 정보</label>
            <input type="text" id="potInfo" placeholder="예: 9cm 화분 / 반에그먼트+야생화흙">

            <label>투입 비료 및 방제 (다중 선택)</label>
            <div class="checkbox-group">
                <label><input type="checkbox" value="마감프K"> 마감프K</label>
                <label><input type="checkbox" value="하이파 멀티코트"> 하이파 멀티코트</label>
                <label><input type="checkbox" value="아그로믹파워"> 아그로믹파워</label>
                <label><input type="checkbox" value="잭스 프로페셔널"> 잭스 프로페셔널</label>
                <label><input type="checkbox" value="벅스킹"> 벅스킹(살충제)</label>
            </div>
        </div>

        <label>개체별 특이사항 (메모)</label>
        <textarea id="plantNote" rows="3" placeholder="이 개체만의 상태나 특징을 적어주세요."></textarea>

        <button onclick="addPlant()">기록 저장하기</button>
    </div>

    <div class="card">
        <h3>🌱 내 식물 관리 일지</h3>
        <div id="plantList"></div>
    </div>

    <script>
        function toggleRepottingFields() {
            const stage = document.getElementById('plantStage').value;
            const repotFields = document.getElementById('repottingFields');
            if(stage === '정식') {
                repotFields.classList.remove('hidden');
            } else {
                repotFields.classList.add('hidden');
            }
        }

        function addPlant() {
            const name = document.getElementById('plantName').value;
            const stage = document.getElementById('plantStage').value;
            const note = document.getElementById('plantNote').value;
            let extras = "";
            let tipsHTML = "";
            let calLink = "";

            if (!name) { alert("식물 이름을 입력해주세요!"); return; }

            // 다중 선택 비료 수집
            let selectedFerts = [];
            const checkboxes = document.querySelectorAll('#repottingFields input[type="checkbox"]:checked');
            checkboxes.forEach((cb) => { selectedFerts.push(cb.value); });

            if (stage === '정식') {
                const pot = document.getElementById('potInfo').value;
                extras = `<p><b>환경:</b> ${pot}</p><p><b>처방:</b> ${selectedFerts.length > 0 ? selectedFerts.join(', ') : '없음'}</p>`;
                
                // 스마트 꿀팁 및 경고 자동 생성
                let tips = "<b>[정식 후 관리 꿀팁]</b><br>• 정식 직후 2~3일은 직사광선을 피해 밝은 그늘에서 적응시켜주세요.<br>";
                if(selectedFerts.includes('벅스킹')) tips += "<span class='warning'>⚠️ [주의] 벅스킹 농약 성분이 있으니 강아지가 흙을 파지 못하게 베란다 접근을 주의하세요.</span><br>";
                if(selectedFerts.includes('아그로믹파워')) tips += "• 아그로믹파워 알약은 연약한 뿌리에 닿지 않게 화분 가장자리에 잘 찔러 넣어주세요.<br>";
                if(selectedFerts.includes('마감프K')) tips += "• 마감프K가 새 뿌리 활착을 도와줄 거에요. 첫 물은 흠뻑 주어 흙을 밀착시켜주세요.<br>";
                
                tipsHTML = `<div class="tips">${tips}</div>`;

                // 구글 캘린더 알람 링크 생성 (임의로 7일 뒤 물주기 알람)
                let date = new Date();
                date.setDate(date.getDate() + 7);
                let dateString = date.toISOString().split('T')[0].replace(/-/g, '');
                let calUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${name}+물주기/상태확인&dates=${dateString}T000000Z/${dateString}T100000Z&details=${name} 정식 후 1주일 경과! 상태를 확인해주세요.`;
                calLink = `<a href="${calUrl}" target="_blank" style="text-decoration:none;"><button class="calendar-btn">📅 구글 캘린더에 물주기 알람 추가</button></a>`;
            }

            const plantDiv = document.createElement('div');
            plantDiv.className = 'plant-item';
            plantDiv.innerHTML = `
                <div class="plant-name">${name} <span style="font-size:0.8em; color:gray;">(${stage})</span></div>
                ${extras}
                <p><b>📝 개체 메모:</b> ${note || "메모 없음"}</p>
                ${tipsHTML}
                ${calLink}
            `;

            document.getElementById('plantList').prepend(plantDiv);

            // 입력 폼 초기화
            document.getElementById('plantName').value = '';
            document.getElementById('plantNote').value = '';
            document.getElementById('potInfo').value = '';
            checkboxes.forEach(cb => cb.checked = false);
        }
    </script>
</body>
</html>
