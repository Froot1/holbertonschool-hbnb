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

document.addEventListener('DOMContentLoaded', () => {
    // Load Header
    fetch('header.html')
      .then(response => response.text())
      .then(data => {
        document.getElementById('header-placeholder').innerHTML = data;
      });
  
    // Load Footer
    fetch('footer.html')
      .then(response => response.text())
      .then(data => {
        document.getElementById('footer-placeholder').innerHTML = data;
      });
  
    // Login form logic
    const loginForm = document.getElementById('login-form');
  
    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
  
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
  
        try {
          const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
          });
  
          if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
          } else {
            const errorData = await response.json();
            alert('Login failed: ' + (errorData?.message || response.statusText));
          }
        } catch (err) {
          console.error('Login error:', err);
          alert('Login failed: Network or server issue');
        }
      });
    }
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
            if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                card.style.display = 'block';
            } else {
        card.style.display = 'none';
      }
    });
  });
}
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (token) {
        console.log('Token found:', token);
        fetchPlaces(token);
      } else {
        console.log('No token found');
      }

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block'; // show login link
    } else {
        loginLink.style.display = 'none';  // hide login link
        fetchPlaces(token); // load places if authenticated
  }
}
  });
  
//   async function fetchPlaces(token) {
//     try {
//       const response = await fetch('http://localhost:5000/api/v1/places/', {
//         method: 'GET',
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       });
  
//       if (!response.ok) {
//         throw new Error('Failed to fetch places');
//       }
  
//       const places = await response.json();
//       displayPlaces(places);
//     } catch (error) {
//       console.error('Error:', error);
//     }
//   }

async function fetchPlaces(token) {
    console.log('fetchPlaces() was called');
    try {
      const response = await fetch('http://localhost:5000/api/v1/places/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (!response.ok) {
        console.error('Response not ok:', response.status, response.statusText);
        throw new Error('Failed to fetch places');
      }
  
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