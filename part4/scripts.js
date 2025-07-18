// Utility functions
function getCookie(name) {
    const cookieArr = document.cookie.split(';');
    for (let cookie of cookieArr) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        return cookie.substring(name.length + 1);
      }
    }
    return null;
  }
  
  function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
  }
  
  function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
      window.location.href = 'index.html'; // redirect unauthenticated users
    }
    return token;
  }
  
  async function fetchPlaces(token) {
    console.log('fetchPlaces() was called');
    try {
      const response = await fetch('http://localhost:5000/api/v1/places/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (!response.ok) throw new Error('Failed to fetch places');
  
      const places = await response.json();
      console.log('Fetched places:', places);
      displayPlaces(places);
    } catch (error) {
      console.error('Error fetching places:', error);
    }
  }
  
  function displayPlaces(places) {
    const list = document.getElementById('places-list');
    list.innerHTML = '';
  
    places.forEach(place => {
      const placeDiv = document.createElement('div');
      placeDiv.classList.add('place-card');
      placeDiv.dataset.price = place.price_by_night;
  
      placeDiv.innerHTML = `
        <h3>${place.name}</h3>
        <p>${place.description || ''}</p>
        <p><strong>Price:</strong> $${place.price_by_night}/night</p>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      `;
  
      list.appendChild(placeDiv);
    });
  }
  
  async function fetchPlaceDetails(token, placeId) {
    try {
      const res = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!res.ok) throw new Error('Failed to fetch place details');
      const place = await res.json();
      displayPlaceDetails(place);
    } catch (err) {
      console.error('Error fetching place details:', err);
    }
  }
  
  function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    detailsSection.innerHTML = `
      <h2>${place.title}</h2>
      <p>${place.description}</p>
      <p><strong>Price:</strong> $${place.price}/night</p>
      <p><strong>Owner:</strong> ${place.owner?.first_name || ''} ${place.owner?.last_name || ''}</p>
      <h3>Amenities:</h3>
      <ul>
        ${place.amenities?.map(a => `<li>${a.name}</li>`).join('') || '<li>None</li>'}
      </ul>
      <h3>Reviews:</h3>
      <ul>
        ${place.reviews?.map(r => `<li><strong>User:</strong> ${r.user_id} | Rating: ${r.rating}<br>${r.text}</li>`).join('') || '<li>No reviews yet.</li>'}
      </ul>
    `;
  }
  
  async function submitReview(token, placeId, reviewText) {
    const res = await fetch('http://localhost:5000/api/v1/reviews/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        place_id: placeId,
        text: reviewText,
        rating: 5, 
        user_id: JSON.parse(atob(token.split('.')[1])).sub // extract from JWT
      })
    });
  
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || 'Unknown error');
    }
  }
  
  // DOM Ready
  document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token'); // 
    const placeId = getPlaceIdFromURL();
  
    // Header + Footer loading
    fetch('header.html')
      .then(res => res.text())
      .then(data => { document.getElementById('header-placeholder').innerHTML = data; });
  
    fetch('footer.html')
      .then(res => res.text())
      .then(data => { document.getElementById('footer-placeholder').innerHTML = data; });
  
    // If on login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
  
        try {
          const res = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
          });
  
          if (res.ok) {
            const data = await res.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
          } else {
            const errorData = await res.json();
            alert('Login failed: ' + (errorData.message || res.statusText));
          }
        } catch (err) {
          alert('Login failed: Network or server issue');
          console.error('Login error:', err);
        }
      });
    }
  
    // Price filter logic
    const filter = document.getElementById('price-filter');
    if (filter) {
      filter.innerHTML = `
        <option value="all">All</option>
        <option value="10">Under $10</option>
        <option value="50">Under $50</option>
        <option value="100">Under $100</option>
      `;
  
      filter.addEventListener('change', () => {
        const selectedPrice = filter.value;
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
          const price = parseFloat(card.dataset.price);
          card.style.display = (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) ? 'block' : 'none';
        });
      });
    }
  
    // Review form handler
    const reviewForm = document.getElementById('review-form');
    if (reviewForm && token && placeId) {
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const reviewText = document.getElementById('review-text').value;
        if (!reviewText) return alert('Please write something!');
        try {
          await submitReview(token, placeId, reviewText);
          alert('✅ Review submitted successfully!');
          reviewForm.reset();
          fetchPlaceDetails(token, placeId);
        } catch (err) {
          alert('❌ Failed to submit review: ' + err.message);
        }
      });
    }
  
    // Load places if authenticated
    const loginLink = document.getElementById('login-link');
    if (token) {
      if (loginLink) loginLink.style.display = 'none';
      if (!placeId) fetchPlaces(token);
    } else {
      if (loginLink) loginLink.style.display = 'block';
    }
  
    // Load place details if on details page
    if (token && placeId) {
      fetchPlaceDetails(token, placeId);
    }
  });
  