const API_BASE = '';

const state = {
  vehicle: 'both',
  sort: 'rating_desc',
  search: ''
};

document.addEventListener('DOMContentLoaded', () => {
  // Vehicle chips
  document.querySelectorAll('.chip-group .chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.chip-group .chip').forEach(c => c.classList.remove('chip-active'));
      chip.classList.add('chip-active');
      state.vehicle = chip.dataset.vehicle;
      fetchDrivers();
    });
  });

  // Sort dropdown
  const sortSelect = document.getElementById('sortSelect');
  sortSelect.addEventListener('change', () => {
    state.sort = sortSelect.value;
    fetchDrivers();
  });

  // Search
  const searchInput = document.getElementById('searchInput');
  const searchBtn = document.getElementById('searchBtn');
  searchBtn.addEventListener('click', () => {
    state.search = searchInput.value.trim();
    fetchDrivers();
  });
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      state.search = searchInput.value.trim();
      fetchDrivers();
    }
  });

  // Modal close
  document.querySelectorAll('[data-close="true"]').forEach(el => {
    el.addEventListener('click', closeModal);
  });

  fetchDrivers();
});

async function fetchDrivers() {
  const params = new URLSearchParams({
    vehicle: state.vehicle,
    sort: state.sort,
    search: state.search
  });

  const res = await fetch(`${API_BASE}/api/drivers?${params.toString()}`);
  const data = await res.json();
  renderDrivers(data);
}

function renderDrivers(drivers) {
  const list = document.getElementById('driversList');
  const empty = document.getElementById('emptyState');
  list.innerHTML = '';

  if (!drivers || drivers.length === 0) {
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  drivers.forEach(d => {
    const card = document.createElement('div');
    card.className = 'driver-card';

    const photo = document.createElement('img');
    photo.className = 'driver-photo';
    photo.src = d.photo_url || 'https://via.placeholder.com/60';
    photo.alt = `${d.name} photo`;

    const info = document.createElement('div');
    info.className = 'driver-info';

    const name = document.createElement('div');
    name.className = 'driver-name';
    name.textContent = d.name;

    const meta = document.createElement('div');
    meta.className = 'driver-meta';
    meta.textContent = `${capitalize(d.vehicle_type)} • ${d.location || 'Parasnath'} • ${d.rides_count || 0} rides`;

    const rating = document.createElement('div');
    rating.className = 'driver-rating';
    rating.textContent = `★ ${Number(d.rating || 0).toFixed(1)} / 5`;

    const actions = document.createElement('div');
    actions.className = 'driver-actions';

    const viewProfile = document.createElement('button');
    viewProfile.className = 'action-btn';
    viewProfile.textContent = 'View profile';
    viewProfile.addEventListener('click', () => openProfile(d.id));

    const addReview = document.createElement('button');
    addReview.className = 'action-btn';
    addReview.textContent = 'Write review';
    addReview.addEventListener('click', () => openProfile(d.id, 'reviews'));

    const reportBtn = document.createElement('button');
    reportBtn.className = 'action-btn';
    reportBtn.textContent = 'Report driver';
    reportBtn.addEventListener('click', () => openProfile(d.id, 'reports'));

    actions.append(viewProfile, addReview, reportBtn);

    info.append(name, meta, rating, actions);

    const right = document.createElement('div');
    right.className = 'driver-right';

    const price = document.createElement('div');
    price.className = 'price';
    price.textContent = d.price ? `₹ ${d.price}` : 'Price on request';

    const callBtn = document.createElement('a');
    callBtn.className = 'call-btn';
    callBtn.href = `tel:${d.phone}`;
    callBtn.textContent = 'Place a call';

    right.append(price, callBtn);

    card.append(photo, info, right);
    list.append(card);
  });
}

function capitalize(s) { return (s || '').charAt(0).toUpperCase() + (s || '').slice(1); }

// Modal handling
function openModal() {
  const m = document.getElementById('profileModal');
  m.classList.add('show');
  m.setAttribute('aria-hidden', 'false');
}
function closeModal() {
  const m = document.getElementById('profileModal');
  m.classList.remove('show');
  m.setAttribute('aria-hidden', 'true');
  document.getElementById('profileContent').innerHTML = '';
}

async function openProfile(driverId, defaultTab = 'reviews') {
  const res = await fetch(`/api/drivers/${driverId}`);
  const driver = await res.json();

  const reviewsRes = await fetch(`/api/reviews?driver_id=${driverId}`);
  const reviews = await reviewsRes.json();

  const reportsRes = await fetch(`/api/reports?driver_id=${driverId}`);
  const reports = await reportsRes.json();

  const content = document.getElementById('profileContent');
  content.innerHTML = `
    <div class="profile-header">
      <img class="profile-photo" src="${driver.photo_url || 'https://via.placeholder.com/56'}" alt="${driver.name} photo" />
      <div>
        <h3 class="profile-title" id="profileTitle">${driver.name}</h3>
        <div class="profile-meta">★ ${Number(driver.rating || 0).toFixed(1)} / 5 • ${capitalize(driver.vehicle_type)} • ${driver.location || 'Parasnath'}</div>
        <div class="profile-meta">Phone: <a href="tel:${driver.phone}">${driver.phone}</a> • Price: ${driver.price ? `₹ ${driver.price}` : 'Ask'}</div>
      </div>
    </div>

    <div class="tabbar">
      <button class="tab-btn ${defaultTab === 'reviews' ? 'active' : ''}" data-tab="reviews">Reviews</button>
      <button class="tab-btn ${defaultTab === 'reports' ? 'active' : ''}" data-tab="reports">Reports</button>
      <button class="tab-btn" data-tab="add-review">Add review</button>
      <button class="tab-btn" data-tab="add-report">Report driver</button>
    </div>

    <div class="tab-content" id="tabContent"></div>
  `;

  const tabContent = document.getElementById('tabContent');
  const renderReviews = () => {
    tabContent.innerHTML = `
      <div class="review-list">
        ${reviews.map(r => `
          <div class="review-item">
            <div class="review-title">Rating: ★ ${Number(r.rating).toFixed(1)} / 5</div>
            <div class="review-meta">${escapeHTML(r.reviewer || 'Anonymous')} • ${new Date(r.created_at).toLocaleString()}</div>
            <div>${escapeHTML(r.text)}</div>
          </div>
        `).join('')}
        ${reviews.length === 0 ? '<div class="review-item">No reviews yet.</div>' : ''}
      </div>
    `;
  };
  const renderReports = () => {
    tabContent.innerHTML = `
      <div class="report-list">
        ${reports.map(p => `
          <div class="report-item">
            <div class="review-title">Report</div>
            <div class="report-meta">${escapeHTML(p.reporter || 'Anonymous')} • ${new Date(p.created_at).toLocaleString()}</div>
            <div>${escapeHTML(p.text)}</div>
          </div>
        `).join('')}
        ${reports.length === 0 ? '<div class="report-item">No reports yet.</div>' : ''}
      </div>
    `;
  };
  const renderAddReview = () => {
    tabContent.innerHTML = `
      <form id="reviewForm">
        <label>
          Your name (optional)
          <input type="text" name="reviewer" class="input" placeholder="Your name" />
        </label>
        <label style="display:block; margin-top:8px;">
          Rating (1-5)
          <input type="number" name="rating" class="input" min="1" max="5" step="1" value="5" required />
        </label>
        <label style="display:block; margin-top:8px;">
          Review
          <textarea name="text" class="input" rows="3" placeholder="Share your experience..." required></textarea>
        </label>
        <button class="btn btn-primary" type="submit" style="margin-top:10px;">Submit review</button>
      </form>
    `;
    const form = document.getElementById('reviewForm');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const payload = {
        driver_id: driverId,
        reviewer: formData.get('reviewer') || '',
        rating: Number(formData.get('rating')),
        text: formData.get('text')
      };
      const res = await fetch('/api/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        const newReviews = await fetch(`/api/reviews?driver_id=${driverId}`).then(r => r.json());
        reviews.splice(0, reviews.length, ...newReviews);
        renderReviews();
      } else {
        alert('Failed to submit review');
      }
    });
  };
  const renderAddReport = () => {
    tabContent.innerHTML = `
      <form id="reportForm">
        <label>
          Your name (optional)
          <input type="text" name="reporter" class="input" placeholder="Your name" />
        </label>
        <label style="display:block; margin-top:8px;">
          Report details
          <textarea name="text" class="input" rows="3" placeholder="Describe the issue..." required></textarea>
        </label>
        <button class="btn btn-primary" type="submit" style="margin-top:10px;">Submit report</button>
      </form>
    `;
    const form = document.getElementById('reportForm');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const payload = {
        driver_id: driverId,
        reporter: formData.get('reporter') || '',
        text: formData.get('text')
      };
      const res = await fetch('/api/reports', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        const newReports = await fetch(`/api/reports?driver_id=${driverId}`).then(r => r.json());
        reports.splice(0, reports.length, ...newReports);
        renderReports();
      } else {
        alert('Failed to submit report');
      }
    });
  };

  // Initial tab render
  if (defaultTab === 'reports') renderReports();
  else renderReviews();

  // Tab switching
  content.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      content.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const tab = btn.dataset.tab;
      if (tab === 'reviews') renderReviews();
      else if (tab === 'reports') renderReports();
      else if (tab === 'add-review') renderAddReview();
      else if (tab === 'add-report') renderAddReport();
    });
  });

  openModal();
}

function escapeHTML(str) {
  return (str || '').replace(/[&<>"'`=\/]/g, s => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;',
    "'": '&#39;', '`': '&#96;', '=': '&#61;', '/': '&#47;'
  }[s]));
}
