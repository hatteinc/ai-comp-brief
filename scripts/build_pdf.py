import os
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = str(Path(__file__).resolve().parent.parent / 'AIカンプ依頼シート.pdf')
FONT = os.environ.get('AI_COMP_FONT', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
if not Path(FONT).is_file():
    raise SystemExit('日本語TrueTypeフォントを AI_COMP_FONT に指定してください。')
pdfmetrics.registerFont(TTFont('Japanese', FONT))
W, H = A4
C = canvas.Canvas(OUT, pagesize=A4)
C.setTitle('AIカンプ依頼シート v0.1')
M = 42
TEAL = '#173A3D'
GRAY = '#526963'

def txt(x, y, value, size=9, color=TEAL):
    C.setFillColor(color); C.setFont('Japanese', size); C.drawString(x, y, value)

def line(y, label, width=495):
    txt(M, y+4, label, 9)
    C.setStrokeColorRGB(.67,.75,.72); C.line(M, y-8, M+width, y-8)

def box(x, y, label):
    C.setStrokeColorRGB(.15,.42,.39); C.rect(x, y-1, 10, 10)
    txt(x+15, y, label, 9)

def header(n, subtitle):
    C.setFillColorRGB(.09,.23,.24); C.rect(0, H-91, W, 91, fill=1, stroke=0)
    txt(M, H-40, 'AIカンプ依頼シート', 19, '#FFFFFF')
    txt(M, H-62, subtitle, 9, '#C8EDE3')
    txt(W-M-30, H-63, f'{n} / 2', 9, '#C8EDE3')

def foot():
    C.setStrokeColorRGB(.75,.81,.79); C.line(M, 42, W-M, 42)
    txt(M, 27, 'v0.1  |  AI Comp Brief  |  文書: CC BY 4.0', 8, GRAY)

header(1, '依頼の意図と支給素材を記録する')
y=H-118
line(y,'案件名'); y-=35
line(y,'依頼者・担当者'); y-=35
line(y,'制作者・担当者'); y-=35
line(y,'作成日 / 用途・公開先'); y-=42
txt(M,y,'01  カンプの基本的な扱い（ひとつ選ぶ）',11); y-=27
box(M,y,'参考のみ  -  構成や雰囲気を参考に、具体的な表現は作り直す'); y-=26
box(M,y,'支給素材を使用  -  指定素材を成果物に使う'); y-=26
box(M,y,'権利処理済みに差替  -  ストック素材・自社素材等に置き換える'); y-=33
line(y,'残したい要素 / 変えてよい要素'); y-=43
txt(M,y,'02  支給素材（素材が複数ある場合はこのページを複写）',11); y-=22
for i in (1,):
    txt(M,y,f'素材 {i}  名称・使用箇所:'); C.line(M+135,y-7,W-M,y-7); y-=27
    txt(M,y,'扱い:'); box(M+52,y,'参考のみ'); box(M+151,y,'そのまま使用'); box(M+282,y,'差替'); y-=26
    txt(M,y,'AI使用:'); box(M+65,y,'あり'); box(M+139,y,'なし'); box(M+212,y,'不明'); y-=26
    line(y,'提供者 / 権利者'); y-=32
    line(y,'AIツール・モデル・版 / 生成日'); y-=32
    line(y,'プロンプト・参照入力（共有不可なら理由）'); y-=32
    line(y,'権利根拠・許諾条件・未確認事項'); y-=45
foot(); C.showPage()

header(2, '確認事項と当事者間の対応をそろえる')
y=H-118
txt(M,y,'03  権利・利用条件の確認',11); y-=26
for label in [
    '素材ごとのAI使用有無、ツール・モデル・プロンプトを記録した',
    '参照元、既存作品、人物・肖像、商標、ロゴ、フォントを確認した',
    '生成サービスとストック素材の利用規約を確認した',
    '商用利用、加工、媒体、地域、期間、二次利用の条件を確認した',
    '未確認事項と追加調査・差替の要否を明示した',
]:
    box(M,y,label); y-=29
y-=12; txt(M,y,'04  担当と対応',11); y-=29
line(y,'支給素材の権利確認担当'); y-=37
line(y,'制作者のAI利用  /  秘密・個人情報のAI入力条件'); y-=37
line(y,'第三者からの申立て時の通知先・公開停止判断'); y-=37
line(y,'申立て時の費用・損害の分担案（個別契約で確定）'); y-=37
line(y,'納品物・編集可能データ・素材情報'); y-=45
txt(M,y,'未確認事項・特記事項',10); y-=18
for _ in range(4):
    C.setStrokeColorRGB(.67,.75,.72); C.line(M,y-6,W-M,y-6); y-=28
y-=13
C.setFillColorRGB(.92,.97,.95); C.roundRect(M,y-73,W-2*M,74,7,fill=1,stroke=0)
txt(M+12,y-16,'重要: このシートは依頼内容の記録です。',9)
txt(M+12,y-34,'権利処理、保証、補償、免責は自動的に成立しません。',9)
txt(M+12,y-52,'必要な分担は個別契約で合意し、第三者からの請求には別途対応してください。',9)
foot(); C.save()
print(OUT)
