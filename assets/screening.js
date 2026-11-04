// PHQ-4 had no Arabic on the previous site. shortcut: new translation, have a clinician check it before relying on it.
Object.assign(SCREEN.ar, {
  phq4_title: 'PHQ-4: فحص الاكتئاب والقلق', phq4_instruction: 'خلال الأسبوعين الماضيين، كم مرة أزعجتك المشكلات التالية؟',
  phq4_q1: 'الشعور بالتوتر أو القلق أو العصبية', phq4_q2: 'عدم القدرة على إيقاف القلق أو السيطرة عليه',
  phq4_q3: 'قلة الاهتمام أو المتعة في القيام بالأشياء', phq4_q4: 'الشعور بالإحباط أو الاكتئاب أو اليأس',
  phq4_results: 'نتائج PHQ-4', phq4_minimal: 'ضيق نفسي بسيط جدًا أو معدوم', phq4_mild: 'ضيق نفسي خفيف', phq4_moderate: 'ضيق نفسي متوسط', phq4_severe: 'ضيق نفسي شديد',
  phq4_minimal_rec: 'تشير إجاباتك إلى ضيق نفسي بسيط جدًا أو معدوم. واصل العناية بنفسك ومتابعة صحتك النفسية.',
  phq4_mild_rec: 'تشير إجاباتك إلى ضيق نفسي خفيف. فكّر في موارد المساعدة الذاتية وتغييرات نمط الحياة التي يمكن أن تحسّن صحتك النفسية.',
  phq4_moderate_rec: 'تشير إجاباتك إلى ضيق نفسي متوسط. فكّر في استشارة مختص في الصحة النفسية لإجراء تقييم كامل.',
  phq4_severe_rec: 'تشير إجاباتك إلى ضيق نفسي شديد. يُرجى طلب المساعدة المهنية لإجراء تقييم شامل ووضع خطة رعاية مناسبة.',
});
const UI = {
  en: { of: (a, b) => `Question ${a} of ${b}`, prev: 'Previous', change: 'Change assessment', score: 'Your score', range: 'Range', note: 'These results are for informational purposes only and do not constitute a diagnosis.', retake: 'Retake', other: 'Try a different assessment', help: 'Find help', safety: 'You told us you have had thoughts of being better off dead or of hurting yourself. You deserve support now. If you might act on these thoughts, call the Royal Oman Police on 9999 or go to the nearest emergency department. Otherwise, please talk to a doctor or someone you trust today.', both: ' Consider using both GAD-7 and PHQ-9 for a more comprehensive assessment.', anx: ' Consider further evaluation with GAD-7 for anxiety.', dep: ' Consider further evaluation with PHQ-9 for depression.' },
  ar: { of: (a, b) => `السؤال ${a} من ${b}`, prev: 'السابق', change: 'تغيير التقييم', score: 'درجتك', range: 'النطاق', note: 'هذه النتائج لأغراض معلوماتية فقط ولا تُعد تشخيصًا.', retake: 'إعادة التقييم', other: 'جرّب تقييمًا آخر', help: 'ابحث عن مساعدة', safety: 'أخبرتنا أنك راودتك أفكار بأنك ستكون أفضل حالًا ميتًا أو بإيذاء نفسك. أنت تستحق الدعم الآن. إذا كنت قد تتصرف بناءً على هذه الأفكار، فاتصل بشرطة عمان السلطانية على 9999 أو توجّه إلى أقرب قسم طوارئ. وإلا فيُرجى التحدث اليوم إلى طبيب أو شخص تثق به.', both: ' فكّر في استخدام GAD-7 وPHQ-9 معًا لتقييم أشمل.', anx: ' فكّر في تقييم إضافي للقلق باستخدام GAD-7.', dep: ' فكّر في تقييم إضافي للاكتئاب باستخدام PHQ-9.' },
};
// Upper score bound of each band, same cut-offs as the previous site.
const BANDS = {
  phq4: [[2, 'minimal'], [5, 'mild'], [8, 'moderate'], [12, 'severe']],
  phq9: [[4, 'minimal'], [9, 'mild'], [14, 'moderate'], [19, 'moderately_severe'], [27, 'severe']],
  gad7: [[4, 'minimal'], [9, 'mild'], [14, 'moderate'], [21, 'severe']],
};
const band = (tool, n) => BANDS[tool].find(b => n <= b[0])[1];
console.assert(band('phq9', 14) === 'moderate' && band('phq9', 15) === 'moderately_severe' && band('gad7', 21) === 'severe' && band('phq4', 2) === 'minimal');

const app = document.getElementById('app'), picker = document.getElementById('picker');
let tool = null, i = 0, ans = [];
const L = () => document.documentElement.lang === 'ar' ? 'ar' : 'en', T = k => SCREEN[L()][k] ?? SCREEN.en[k];
const el = (tag, props = {}, ...kids) => { const n = Object.assign(document.createElement(tag), props); n.append(...kids); return n; };
const btn = (text, fn) => el('button', { className: 'btn ghost', type: 'button', textContent: text, onclick: fn });

function render() {
  app.innerHTML = '';
  picker.style.display = tool ? 'none' : '';
  if (!tool) return;
  const qs = SCREEN.q[tool], u = UI[L()];
  if (i < qs.length) {
    const opts = [0, 1, 2, 3].map(v => {
      const b = el('button', { className: 'opt', type: 'button', textContent: T('opt' + v), onclick() { ans[i] = v; i++; render(); } });
      b.setAttribute('aria-pressed', ans[i] === v); return b;
    });
    const h = el('h2', { textContent: T(qs[i]), tabIndex: -1 }); h.style.fontSize = 'clamp(24px,3vw,34px)';
    const bar = el('div', { className: 'bar' }, el('i')); bar.firstChild.style.width = (i / qs.length * 100) + '%';
    app.append(el('p', { className: 'eyebrow', textContent: T(tool + '_title') }), el('p', { textContent: `${u.of(i + 1, qs.length)} · ${T(tool + '_instruction')}` }), bar, h, ...opts,
      el('div', { className: 'btns' }, ...(i ? [btn(u.prev, () => { i--; render(); })] : []), btn(u.change, () => { tool = null; render(); })));
    h.focus({ preventScroll: true });
    return;
  }
  const sum = ans.reduce((a, b) => a + b, 0), b = band(tool, sum);
  let rec = T(`${tool}_${b}_rec`);
  if (tool === 'phq4') {
    const a = ans[0] + ans[1], d = ans[2] + ans[3];
    rec += a >= 3 && d >= 3 ? u.both : a >= 3 ? u.anx : d >= 3 ? u.dep : '';
  }
  const res = el('div', { className: 'card' }, el('h2', { textContent: T(tool + '_results') }), el('p', { textContent: u.score }), el('div', { className: 'score', textContent: sum }),
    el('p', { textContent: `${u.range}: 0–${BANDS[tool].at(-1)[0]}` }), el('h3', { textContent: T(`${tool}_${b}`) }), el('p', { textContent: rec }), el('p', { textContent: u.note }));
  if (tool === 'phq9' && ans[8] > 0) res.prepend(el('div', { className: 'alert', role: 'alert', textContent: u.safety }));
  res.append(el('div', { className: 'btns' }, el('a', { className: 'btn', href: 'index.html#contact', textContent: u.help }), btn(u.retake, () => { i = 0; ans = []; render(); }), btn(u.other, () => { tool = null; render(); })));
  app.append(res);
}
document.querySelectorAll('[data-tool]').forEach(c => c.onclick = () => { tool = c.dataset.tool; i = 0; ans = []; render(); scrollTo({ top: app.offsetTop - 110 }); });
document.addEventListener('langchange', render);
