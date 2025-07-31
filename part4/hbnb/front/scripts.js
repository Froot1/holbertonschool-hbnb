const API_CONFIG = {
    host: 'http://127.0.0.1',
    port: '5000',
    version: 'v1'
};
const apiUrl = `${API_CONFIG.host}:${API_CONFIG.port}/api/${API_CONFIG.version}`;


function setCookie(name, value, days) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = `expires=${date.toUTCString()}`;
  document.cookie = `${name}=${value}; ${expires}; path=/; domain=${window.location.hostname}`;
}

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return value;
  }
  return null;
}

function parseJwt(token) {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  return JSON.parse(jsonPayload);
}

window.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname.includes('login.html') && getCookie('hbnb_token')) {
    window.location.href = 'index.html';
  }
});

window.addEventListener('load', () => {
  checkAuthentication()
});

async function checkAuthentication() {
  const token = getCookie('hbnb_token');

  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
    }
  }
  const placesList = document.getElementById('places-list');
  if (placesList) {
    fetchPlaces();
  }

  const addReviewForm = document.querySelector('#add-review-form');
  if (addReviewForm) {
    addReviewForm.style.display = token ? 'block' : 'none';
  }

  const placeId = getPlaceIdFromURL();
  if (placeId) {
    await fetchPlaceDetails(placeId, token);
  }
}

function validateInput(password) {
  if (!password || password.length < 6) {
    throw new Error('Password too short');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = loginForm.querySelector('[name="email"]').value;
      const password = loginForm.querySelector('[name="password"]').value;

      try {
        validateInput(password);
        const response = await fetch(`${apiUrl}/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          setCookie('hbnb_token', data.access_token, 1);
          window.location.href = 'index.html';
        } else {
          const error = await response.json();
          alert('Login failed: ' + (error.message || response.statusText));
        }
      } catch (error) {
        alert('Login failed: ' + error.message);
      }
    });
  }
});

async function fetchPlaces() {
  try {
    const response = await fetch(`${apiUrl}/places`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    displayPlaces(data);
  } catch (error) {
    console.error('Error: ', error);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  places.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.classList.add('place-card');
    const placeInfo = `
      <div class="place-info">
          <h2>${place.name}</h2>
          <p>Price per night: $${place.price_by_night}</p>
      </div>
      <a href="place.html?id=${place.id}"><button class="details-button">View Details</button></a>
    `;
    placeCard.innerHTML = placeInfo;
    placesList.appendChild(placeCard);
  });
}

const priceFilter = document.getElementById('price-filter');
if (priceFilter) {
  const options = ['All', '$10', '$50', '$100'];

  options.forEach(option => {
    const opt = document.createElement('option');
    opt.value = option === 'All' ? '' : parseInt(option.replace('$', ''));
    opt.textContent = option;
    priceFilter.appendChild(opt);
  });

  priceFilter.addEventListener('change', (event) => {
    const selectedPrice = event.target.value ? parseInt(event.target.value) : Infinity;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
      const priceText = card.querySelector('.place-info p').textContent;
      const price = parseInt(priceText.replace('Price per night: $', ''));
      if (price <= selectedPrice) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

async function fetchPlaceDetails(placeId, token) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${apiUrl}/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });

    if (response.status === 404) {
      const placeDetails = document.querySelector('#place-details');
      if (placeDetails) {
        placeDetails.innerHTML = '<h1>Place not found</h1><p>The requested place does not exist.</p>';
      }
      return;
    }

    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }

    const placeData = await response.json();
    displayPlaceDetails(placeData);
  } catch (error) {
    console.error('Error:', error);
    const placeDetails = document.querySelector('#place-details');
    if (placeDetails) {
      placeDetails.innerHTML = '<h1>Error</h1><p>Failed to load place details. Please try again later.</p>';
    }
  }
}

async function fetchUserName(userId) {
  try {
    const response = await fetch(`${apiUrl}/users/${userId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch user details');
    }
    const userData = await response.json();
    return userData.first_name + ' ' + userData.last_name;
  } catch (error) {
    console.error('Error:', error);
    return 'Unknown User';
  }
}

async function displayPlaceDetails(place) {
  const placeDetails = document.querySelector('#place-details');
  if (!placeDetails) return;

  // Map amenity names to icon filenames
  const amenityIconMap = {
    "Air Conditioning": "icon_Air_Conditioning.png",
    "Bath": "icon_bath.png",
    "Bed": "icon_bed.png",
    "Swimming Pool": "icon_swimming_pool.png",
    "WiFi": "icon_wifi.png"
    // Add more mappings as needed
  };

  let html = `
  <div class="details-card">
    <h2>${place.title}</h2>
    <p><b>Host:</b> ${place.owner.first_name + ' ' + place.owner.last_name}</p>
    <p><b>Price per night:</b> $${parseInt(place.price)}</p>
    <p><b>Description:</b> ${place.description}</p>
    <p><b>Amenities:</b> 
      <span>
        ${place.amenities.map(amenity => {
          const iconFile = amenityIconMap[amenity.name];
          if (iconFile) {
            return `<img src="images/${iconFile}" alt="${amenity.name}" title="${amenity.name}" style="height:24px;vertical-align:middle;margin-right:4px;">${amenity.name}`;
          } else {
            return amenity.name;
          }
        }).join(', ')}
      </span>
    </p>
  </div>
  `;

  const reviewsHtml = place.reviews && place.reviews.length ? await Promise.all(place.reviews.map(async review => {
    const userName = await fetchUserName(review.user_id);
    return `
      <div class="review-card">
        <p><b>${userName}</b></p>
        <p>${review.text}</p>
        <p><b>Rating:</b> <span class="star-rating">${'★'.repeat(review.rating)}</span></p>
      </div>
    `;
  })).then(reviews => reviews.join('')) : '<div class="review-card"><p><b>No reviews yet</b></p></div>';

  html += reviewsHtml;

  placeDetails.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = getCookie('hbnb_token');

  if (reviewForm) {
    reviewForm.style.display = token ? 'block' : 'none';
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = getCookie('hbnb_token');

  if (reviewForm) {
    if (!token) {
      reviewForm.style.display = 'none';
      return;
    }

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
      window.location.href = 'index.html';
      return;
    }

    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      
      const reviewText = reviewForm.querySelector('#review').value;
      const rating = reviewForm.querySelector('#rating').value;

      try {
        const response = await fetch(`${apiUrl}/reviews/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            text: reviewText,
            rating: parseInt(rating),
            user_id: parseJwt(token).sub,
            place_id: placeId.toString()         
          })
        });

        if (response.ok) {
          const messageDiv = document.createElement('div');
          messageDiv.className = 'success-message';
          messageDiv.textContent = 'Review submitted successfully!';
          reviewForm.insertBefore(messageDiv, reviewForm.firstChild);
          
          reviewForm.querySelector('#review').value = '';
          reviewForm.querySelector('#rating').value = '';
          
          await fetchPlaceDetails(placeId, token);
          
          setTimeout(() => messageDiv.remove(), 3000);
        } else {
          throw new Error('Failed to submit review');
        }
      } catch (error) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'error-message';
        messageDiv.textContent = error.message;
        reviewForm.insertBefore(messageDiv, reviewForm.firstChild);
        
        setTimeout(() => messageDiv.remove(), 3000);
      }
    });
  }
});
