// ===============================
// CONFIG
// ===============================
const API_BASE = 'http://127.0.0.1:8002'; // 

// ===============================
// ELEMENTS
// ===============================
const amountInput = document.getElementById('amountInput');
const amountRange = document.getElementById('amountRange');
const daysInput = document.getElementById('daysInput');
const daysRange = document.getElementById('daysRange');

const stepLoan = document.getElementById('step-loan');
const stepForm = document.getElementById('step-form');
const stepDecision = document.getElementById('step-decision');

const toFormBtn = document.getElementById('toFormBtn');
const submitBtn = document.getElementById('submitBtn');

const firstName = document.getElementById('firstName');
const lastName = document.getElementById('lastName');
const middleName = document.getElementById('middleName');
const birthDate = document.getElementById('birthDate');
const passport = document.getElementById('passport');
const phone = document.getElementById('phone');

// ===============================
// UI STATE
// ===============================
let id = null;
let decision = null;
let approved_amount = null;
let approved_days = null;
let reject_reason = null;

// ===============================
// RANGE SYNC
// ===============================
amountInput.oninput = () => amountRange.value = amountInput.value;
amountRange.oninput = () => amountInput.value = amountRange.value;

daysInput.oninput = () => daysRange.value = daysInput.value;
daysRange.oninput = () => daysInput.value = daysRange.value;

// ===============================
// STEP SWITCH
// ===============================
toFormBtn.onclick = () => {
  stepLoan.classList.add('hidden');
  stepForm.classList.remove('hidden');

  document.getElementById('mainTitle').innerText =
    'Введите свои персональные данные';

  document.getElementById('subtitle').innerText = '';
};

// ===============================
// VALIDATION HELPERS
// ===============================
function onlyCyrillic(input) {
  input.addEventListener('input', () => {
    input.value = input.value.replace(/[^а-яА-ЯёЁ]/g, '');
  });
}

onlyCyrillic(firstName);
onlyCyrillic(lastName);
onlyCyrillic(middleName);

// ===============================
// PASSPORT MASK (1234 567890)
// ===============================
passport.addEventListener('input', () => {
  let digits = passport.value.replace(/\D/g, '').slice(0, 10);
  passport.value = digits.length <= 4
    ? digits
    : digits.slice(0, 4) + ' ' + digits.slice(4);
});

// ===============================
// PHONE MASK +7(___)___-__-__
// ===============================
phone.addEventListener('focus', () => {
  if (!phone.value) phone.value = '+7';
});

phone.addEventListener('input', () => {
  let digits = phone.value.replace(/\D/g, '');
  if (digits[0] !== '7') digits = '7' + digits;
  digits = digits.slice(0, 11);

  let result = '+7';
  if (digits.length > 1) result += '(' + digits.slice(1, 4);
  if (digits.length >= 4) result += ')';
  if (digits.length >= 5) result += digits.slice(4, 7);
  if (digits.length >= 8) result += '-' + digits.slice(7, 9);
  if (digits.length >= 10) result += '-' + digits.slice(9, 11);

  phone.value = result;
});

// ===============================
// SUBMIT APPLICATION
// ===============================
submitBtn.onclick = async () => {
  submitBtn.disabled = true;
  submitBtn.textContent = 'Отправляем...';

  try {
    const payload = {
      first_name: firstName.value.trim(),
      last_name: lastName.value.trim(),
      middle_name: middleName.value.trim() || null,
      birth_date: birthDate.value,
      passport_number: passport.value,
      phone_number: phone.value.replace(/\D/g, ''),
      requested_amount: Number(amountInput.value),
      requested_days: Number(daysInput.value),
    };

    const res = await fetch(`${API_BASE}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error('Application error');

    const data = await res.json();

    id = data.id;
    decision = data.decision;
    approved_amount = data.approved_amount;
    approved_days = data.approved_days;
    reject_reason = data.reject_reason;

    renderDecision();

  } catch (e) {
    alert('Ошибка отправки заявки. Попробуйте позже.');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Получить решение';
  }
};

// ===============================
// COUNTER ACTIONS
// ===============================
async function acceptCounter() {
  stepDecision.innerHTML = '<p>Подтверждаем условия...</p>';

  try {
    const res = await fetch(
      `${API_BASE}/applications/${id}/counter/accept`,
      { method: 'POST' }
    );

    if (!res.ok) throw new Error();

    const data = await res.json();

    decision = data.decision;
    approved_amount = data.approved_amount;
    approved_days = data.approved_days;

    renderDecision();

  } catch {
    alert('Контр-предложение недоступно');
  }
}

async function rejectCounter() {
  await fetch(
    `${API_BASE}/applications/${id}/counter/reject`,
    { method: 'POST' }
  );

  decision = 'REJECT';
  reject_reason = 'Вы отказались от предложенных условий';
  renderDecision();
}

// ===============================
// RENDER DECISION
// ===============================
function renderDecision() {
  stepForm.classList.add('hidden');
  stepDecision.classList.remove('hidden');

  if (decision === 'APPROVED') {
    stepDecision.innerHTML = `
      <div class="status-approved">Заявка одобрена</div>
      <p>Сумма: ${approved_amount} ₽</p>
      <p>Срок: ${approved_days} дней</p>
      <button class="primary-btn">Оформить займ</button>
    `;
  }

  if (decision === 'COUNTER') {
    stepDecision.innerHTML = `
      <div class="status-counter">Мы готовы выдать займ на других условиях</div>
      <p>Сумма: ${approved_amount} ₽</p>
      <p>Срок: ${approved_days} дней</p>
      <button id="acceptBtn" class="primary-btn">Принять условия</button>
      <button id="rejectBtn" class="primary-btn secondary-btn">Отказаться</button>
    `;

    document.getElementById('acceptBtn').onclick = acceptCounter;
    document.getElementById('rejectBtn').onclick = rejectCounter;
  }

  if (decision === 'REJECT') {
    stepDecision.innerHTML = `
      <div class="status-reject">К сожалению, мы не можем выдать займ</div>
      ${reject_reason ? `<p>${reject_reason}</p>` : ''}
    `;
  }
}
