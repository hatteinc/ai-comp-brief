const form = document.querySelector('#brief');
const materials = document.querySelector('#materials');
const result = document.querySelector('#result');
const status = document.querySelector('#status');
const template = document.querySelector('#material-template');

function addMaterial() {
  materials.append(template.content.cloneNode(true));
  renumber();
  update();
}
function renumber() {
  [...materials.querySelectorAll('.material-number')].forEach((n, i) => { n.textContent = String(i + 1); });
}
function value(name) { return String(new FormData(form).get(name) || '').trim() || '未記入'; }
function field(row, name) { return row.querySelector(`[data-field="${name}"]`).value.trim() || '未記入'; }
function update() {
  const modes = [...form.querySelectorAll('[name="mode"]')];
  const mode = modes.find(x => x.checked)?.value || '未選択';
  const rows = [...materials.querySelectorAll('.material')];
  const checked = [...form.querySelectorAll('.checks input')].map(x => `- [${x.checked ? 'x' : ' '}] ${x.parentElement.textContent.trim()}`).join('\n');
  const items = rows.map((row, i) => `### 素材 ${i + 1}: ${field(row, 'name')}\n- 扱い: ${field(row, 'handling')}\n- 生成AI使用: ${field(row, 'ai')}\n- 提供者・権利者: ${field(row, 'provider')}\n- ツール・モデル・版: ${field(row, 'model')}\n- 生成日: ${field(row, 'generated')}\n- プロンプト・参照入力または非共有理由: ${field(row, 'prompt')}\n- 権利根拠・許諾条件・未確認事項: ${field(row, 'rights')}`).join('\n\n');
  result.value = `# AIカンプ依頼シート\n\n- 案件名: ${value('project')}\n- 依頼者: ${value('client')}\n- 制作者: ${value('creator')}\n- 作成日: ${value('date')}\n- 用途・公開先: ${value('usage')}\n\n## カンプの扱い\n- 基本指定: ${mode}\n- 残したい要素・変えてよい要素: ${value('direction')}\n\n## 支給素材\n${items || '素材なし'}\n\n## 権利と作業の分担\n- 支給素材の権利確認担当: ${value('rightsOwner')}\n- 第三者申立ての連絡先: ${value('claimContact')}\n- 差替素材の費用負担: ${value('replacementCost')}\n- 支給素材に起因する申立ての費用・損害の分担案: ${value('liability')}\n- 制作者のAI利用: ${value('creatorAI')}\n- 機密・個人情報のAI入力: ${value('dataPolicy')}\n- 未確認事項・懸念: ${value('openIssues')}\n- 納品物・追加条件: ${value('deliverables')}\n\n## 依頼前チェック\n${checked}\n\n## 合意に関する注意\nこのシートは依頼内容の記録であり、権利処理、保証、補償、免責を自動的に成立させるものではありません。未確認事項と第三者申立て時の通知・調査・公開停止・差替・費用負担は、当事者間の契約で具体的に合意してください。\n`;
  document.querySelector('#print-result').textContent = result.value;
}
form.addEventListener('input', update);
form.addEventListener('change', update);
materials.addEventListener('click', e => {
  if (e.target.matches('.remove')) { e.target.closest('.material').remove(); renumber(); update(); }
});
document.querySelector('#add-material').addEventListener('click', addMaterial);
document.querySelector('#copy').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(result.value); status.textContent = 'コピーしました。'; }
  catch { result.select(); status.textContent = 'コピーできませんでした。依頼文を選択してコピーしてください。'; }
});
document.querySelector('#download').addEventListener('click', () => {
  const blob = new Blob([result.value], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = 'ai-comp-brief.md'; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
document.querySelector('#print').addEventListener('click', () => window.print());
const today = new Date();
form.elements.date.value = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
addMaterial();
