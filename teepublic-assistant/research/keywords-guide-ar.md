# دليل ملف تسجيل الكلمات وGoogle Trends

الهدف: أن ترتّب أفكار تصاميمك حسب **أرقام قستها بنفسك**، وليس حسب تقديرات المقالات.

- **الطلب**: كم يبحث الناس عن الكلمة، ومصدره Google Trends.
- **المنافسة**: كم تصميماً موجوداً لنفس الكلمة، ومصدرها عدد النتائج في TeePublic وEtsy.

---

## الخطوة 1: أنشئ ملف الكلمات (مرة واحدة)

```bash
python -m teepublic_assistant keywords init
```
ينشئ ملف `keywords.csv` يمكنك فتحه في Excel أو Google Sheets.

## الخطوة 2: سجّل المنافسة (عدد النتائج)

1. افتح teepublic.com واكتب الكلمة في البحث، مثل `pickleball shirt`.
2. انظر إلى عدد النتائج المكتوب أعلى الصفحة.
3. سجّله:
```bash
python -m teepublic_assistant keywords add "pickleball shirt" --teepublic 3200
python -m teepublic_assistant keywords add "mahjong shirt" --teepublic 640 --etsy 9800
```
يمكنك أيضاً كتابة الأرقام مباشرة في الملف داخل Excel.

> اكتب الكلمة بالإنجليزية وبنفس الصيغة في كل مكان، لأن المشترين على TeePublic يبحثون بالإنجليزية.

## الخطوة 3: سجّل الطلب من Google Trends

1. افتح [trends.google.com](https://trends.google.com).
2. اكتب حتى **5 كلمات** للمقارنة بينها.
3. اختر الإعدادات:
   - البلد: **United States**، أو البلد الذي تبيع له أكثر.
   - المدة: **Past 2 years**، لأن الأداة تحتاج سنة سابقة للمقارنة.
   - المصدر: **Web Search**.
4. في رسم «Interest over time» اضغط زر **التنزيل ⬇** فتحصل على ملف `multiTimeline.csv`.
5. استورده:
```bash
python -m teepublic_assistant keywords trends multiTimeline.csv
```
الأداة تحسب لكل كلمة:
- **trend_recent**: متوسط الاهتمام في آخر 3 أشهر (من 0 إلى 100).
- **trend_growth**: هل الاهتمام صاعد أم نازل مقارنة بنفس الفترة من السنة الماضية (2.0x تعني ضعف السنة الماضية).
- **peak_month**: الشهر الذي يكون فيه الاهتمام في أعلى مستوى.

### ⚠️ قاعدة مهمة في Google Trends
أرقام Google Trends **نسبية داخل الملف الواحد فقط**. الرقم 100 يعني أعلى نقطة بين الكلمات التي قارنتها معاً، فلا يصح مقارنة رقم من ملف بآخر من ملف مختلف.

**الحل:** ضع **كلمة ثابتة** في كل مقارنة، مثل `cat shirt`، ثم أضف معها 4 كلمات جديدة. هكذا تبقى الأرقام قابلة للمقارنة تقريباً. وستنبّهك الأداة إذا جاءت الأرقام من ملفات مختلفة.

## الخطوة 4: رتّب الكلمات

```bash
python -m teepublic_assistant keywords score
```
مثال على النتيجة (من البيانات التجريبية الوهمية):
```
 #  keyword                score  trend  growth  results  peak       verdict
 1  mahjong shirt          241.7   37.2   3.34x      640  September  opportunity: demand with little competition
 2  pickleball shirt       194.8   61.1   1.25x    3,200  August     ok
 3  nurse christmas shirt   11.9    5.1   0.99x   18,500  December   seasonal: peaks in December, upload now
```

**معنى التقييم (verdict):**
| التقييم | المعنى | ماذا تفعل |
|---|---|---|
| `opportunity` | طلب حقيقي ومنافسة قليلة (أقل من 2000 نتيجة) | صمّم لها أولاً |
| `seasonal … upload now` | طلبها يرتفع خلال 1–3 أشهر | ارفع الآن حتى تظهر في البحث قبل الموسم |
| `rising` | الاهتمام زاد 50% أو أكثر عن السنة الماضية | فرصة صاعدة |
| `falling` | الاهتمام انخفض كثيراً | تجنّبها |
| `crowded` | أكثر من 100 ألف نتيجة | ضيّقها: أضف مهنة أو حيواناً أو مناسبة |
| `needs …` | بيانات ناقصة | أكمل الرقم الناقص |

**كيف يُحسب الرقم (score):** الطلب × الصعود ÷ المنافسة. المنافسة محسوبة على مقياس لوغاريتمي، أي أن الفرق بين 1000 و10000 نتيجة أهم من الفرق بين 100 ألف و110 آلاف. هذه **قاعدة تقريبية للترتيب** وليست ضماناً للمبيعات.

## الخطوة 5: أغلق الدائرة بمبيعاتك

بعد أن ترفع تصاميم للكلمات الأعلى تقييماً، انتظر 4–6 أسابيع، ثم شغّل:
```bash
python -m teepublic_assistant report my_sales.csv
```
المبيعات الحقيقية هي الحقيقة المؤكدة الوحيدة. اصنع نسخاً إضافية من الرابح فقط.

## تجربة سريعة بالبيانات الوهمية
```bash
python -m teepublic_assistant keywords init test.csv
python -m teepublic_assistant keywords add "mahjong shirt" --teepublic 640 -f test.csv
python -m teepublic_assistant keywords trends sample_data/sample_google_trends.csv -f test.csv
python -m teepublic_assistant keywords score -f test.csv
```
