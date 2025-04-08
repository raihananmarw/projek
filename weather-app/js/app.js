const apiKey = '8cfea8758e7bce55080a3c2302c8c6ec'; // Ganti dengan API key Anda
const searchBtn = document.getElementById('search-btn');
const cityInput = document.getElementById('city-input');
const temperature = document.getElementById('temperature');
const condition = document.getElementById('condition');
const humidity = document.getElementById('humidity');
const wind = document.getElementById('wind');

searchBtn.addEventListener('click', function() {
    const city = cityInput.value;
    if (city) {
        getWeatherData(city);
    }
});

async function getWeatherData(city) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric&lang=id`);
        const data = await response.json();
        
        if (data.cod === 200) {
            // Menampilkan data cuaca
            temperature.textContent = `Suhu: ${data.main.temp}°C`;
            condition.textContent = `Kondisi: ${data.weather[0].description}`;
            humidity.textContent = `Kelembapan: ${data.main.humidity}%`;
            wind.textContent = `Kecepatan Angin: ${data.wind.speed} m/s`;
        } else {
            alert('Kota tidak ditemukan!');
        }
    } catch (error) {
        console.error(error);
        alert('Terjadi kesalahan. Coba lagi!');
    }
}

const forecastContainer = document.getElementById('forecast');

async function getWeatherData(city) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric&lang=id`);
        const data = await response.json();
        
        if (data.cod === 200) {
            // Menampilkan data cuaca saat ini
            temperature.textContent = `Suhu: ${data.main.temp}°C`;
            condition.textContent = `Kondisi: ${data.weather[0].description}`;
            humidity.textContent = `Kelembapan: ${data.main.humidity}%`;
            wind.textContent = `Kecepatan Angin: ${data.wind.speed} m/s`;
            
            // Mendapatkan perkiraan cuaca 5 hari
            getForecastData(city);
        } else {
            alert('Kota tidak ditemukan!');
        }
    } catch (error) {
        console.error(error);
        alert('Terjadi kesalahan. Coba lagi!');
    }
}

async function getForecastData(city) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${apiKey}&units=metric&lang=id`);
        const data = await response.json();

        if (data.cod === "200") {
            // Mengelompokkan data berdasarkan tanggal
            const forecastGroupedByDate = groupByDate(data.list);

            forecastContainer.innerHTML = ''; // Clear sebelumnya

            // Menampilkan cuaca untuk 5 hari
            Object.keys(forecastGroupedByDate).slice(0, 5).forEach(date => {
                const dayForecast = forecastGroupedByDate[date][0]; // Ambil data pertama dari setiap hari
                const dateObj = new Date(dayForecast.dt * 1000); // Convert timestamp ke format tanggal
                const day = dateObj.toLocaleDateString('id-ID', { weekday: 'long' });

                const forecastItem = document.createElement('div');
                forecastItem.classList.add('forecast-item');
                forecastItem.innerHTML = `
                    <p>${day}</p>
                    <p>${dayForecast.main.temp}°C</p>
                    <p>${dayForecast.weather[0].description}</p>
                `;
                
                forecastContainer.appendChild(forecastItem);
            });
        }
    } catch (error) {
        console.error(error);
        alert('Terjadi kesalahan saat mengambil perkiraan cuaca.');
    }
}

// Fungsi untuk mengelompokkan data cuaca berdasarkan tanggal
function groupByDate(data) {
    return data.reduce((acc, curr) => {
        const date = new Date(curr.dt * 1000).toLocaleDateString('id-ID'); // Format hanya tanggal
        if (!acc[date]) acc[date] = [];
        acc[date].push(curr);
        return acc;
    }, {});
}

// Geolokasi Otomatis
document.addEventListener("DOMContentLoaded", () => {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                getWeatherByLocation(lat, lon);
            },
            (error) => {
                console.error("Gagal mendapatkan lokasi:", error);
                alert("Tidak dapat mengakses lokasi. Izinkan akses lokasi untuk mendapatkan cuaca otomatis.");
            }
        );
    } else {
        alert("Geolokasi tidak didukung di browser ini.");
    }
});

async function getWeatherByLocation(lat, lon) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric&lang=id`);
        const data = await response.json();

        if (data.cod === 200) {
            // Tampilkan nama kota berdasarkan koordinat
            cityInput.value = data.name;

            // Tampilkan cuaca
            temperature.textContent = `Suhu: ${data.main.temp}°C`;
            condition.textContent = `Kondisi: ${data.weather[0].description}`;
            humidity.textContent = `Kelembapan: ${data.main.humidity}%`;
            wind.textContent = `Kecepatan Angin: ${data.wind.speed} m/s`;

            // Ambil perkiraan cuaca
            getForecastData(data.name);
        } else {
            alert("Gagal mengambil data cuaca.");
        }
    } catch (error) {
        console.error("Error mengambil cuaca berdasarkan lokasi:", error);
        alert("Terjadi kesalahan. Coba lagi.");
    }
}

// Peta Interaktif
// Inisialisasi Peta
let map = L.map("map").setView([0, 0], 2); // Posisi awal (0,0) dengan zoom level 2

// Tambahkan Tile Layer dari OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors"
}).addTo(map);

// Fungsi untuk menampilkan cuaca di peta
async function showWeatherOnMap(lat, lon) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric&lang=id`);
        const data = await response.json();

        if (data.cod === 200) {
            // Tambahkan marker ke peta
            L.marker([lat, lon]).addTo(map)
                .bindPopup(`
                    <b>${data.name}</b><br>
                    Suhu: ${data.main.temp}°C<br>
                    ${data.weather[0].description}
                `)
                .openPopup();

            // Update posisi peta
            map.setView([lat, lon], 10);
        }
    } catch (error) {
        console.error("Error saat menampilkan cuaca di peta:", error);
    }
}

// Panggil showWeatherOnMap saat pengguna memasukkan kota
async function getWeatherData(city) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric&lang=id`);
        const data = await response.json();
        
        if (data.cod === 200) {
            temperature.textContent = `Suhu: ${data.main.temp}°C`;
            condition.textContent = `Kondisi: ${data.weather[0].description}`;
            humidity.textContent = `Kelembapan: ${data.main.humidity}%`;
            wind.textContent = `Kecepatan Angin: ${data.wind.speed} m/s`;

            // Tampilkan cuaca di peta
            showWeatherOnMap(data.coord.lat, data.coord.lon);

            // Ambil perkiraan cuaca
            getForecastData(city);
        } else {
            alert('Kota tidak ditemukan!');
        }
    } catch (error) {
        console.error(error);
        alert('Terjadi kesalahan. Coba lagi!');
    }
}

// Alert Cuaca
async function checkExtremeWeather(city) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric&lang=id`);
        const data = await response.json();

        if (data.cod === 200) {
            const temp = data.main.temp;
            const windSpeed = data.wind.speed;
            const condition = data.weather[0].main.toLowerCase(); // Contoh: "rain", "thunderstorm", "snow"

            let warningMessage = "";

            // Deteksi kondisi ekstrem
            if (temp > 38) {
                warningMessage += "🔥 Suhu sangat panas! Tetap terhidrasi. ";
            } else if (temp < 5) {
                warningMessage += "❄️ Suhu sangat dingin! Kenakan pakaian hangat. ";
            }

            if (windSpeed > 15) {
                warningMessage += "🌬️ Angin kencang! Hati-hati saat bepergian. ";
            }

            if (condition.includes("thunderstorm")) {
                warningMessage += "⛈️ Badai petir! Sebaiknya tetap di dalam ruangan. ";
            } else if (condition.includes("rain")) {
                warningMessage += "☔ Hujan lebat! Siapkan payung atau jas hujan. ";
            }

            if (warningMessage) {
                showExtremeWeatherAlert(warningMessage);
            }
        }
    } catch (error) {
        console.error("Error memeriksa cuaca ekstrem:", error);
    }
}

// Fungsi untuk menampilkan peringatan cuaca ekstrem
function showExtremeWeatherAlert(message) {
    const alertBox = document.createElement("div");
    alertBox.classList.add("weather-alert");
    alertBox.innerHTML = `<p>${message}</p><button onclick="this.parentElement.remove()">Tutup</button>`;

    document.body.appendChild(alertBox);
}

async function getWeatherData(city) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric&lang=id`);
        const data = await response.json();
        
        if (data.cod === 200) {
            temperature.textContent = `Suhu: ${data.main.temp}°C`;
            condition.textContent = `Kondisi: ${data.weather[0].description}`;
            humidity.textContent = `Kelembapan: ${data.main.humidity}%`;
            wind.textContent = `Kecepatan Angin: ${data.wind.speed} m/s`;

            // Tampilkan cuaca di peta
            showWeatherOnMap(data.coord.lat, data.coord.lon);

            // Cek peringatan cuaca ekstrem
            checkExtremeWeather(city);

            // Ambil perkiraan cuaca
            getForecastData(city);
        } else {
            alert('Kota tidak ditemukan!');
        }
    } catch (error) {
        console.error(error);
        alert('Terjadi kesalahan. Coba lagi!');
    }
}

// Mode Gelap
const darkModeToggle = document.getElementById("dark-mode-toggle");

// Cek apakah mode gelap sebelumnya telah diaktifkan
if (localStorage.getItem("dark-mode") === "enabled") {
    document.body.classList.add("dark-mode");
}

// Event listener untuk tombol mode gelap
darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    // Simpan preferensi mode gelap ke localStorage
    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("dark-mode", "enabled");
    } else {
        localStorage.setItem("dark-mode", "disabled");
    }
});